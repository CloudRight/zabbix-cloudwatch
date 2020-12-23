#!/usr/bin/env python3
import argparse
import datetime
import os

from discovery.aws_client import AWSClient


class Checker(AWSClient):
    def get_metric(self, interval, metric, namespace, statistic, history, dimensions):
        history = int(history)

        # Constructing timestamps for limiting CloudWatch datapoint list
        time_delay = datetime.timedelta(seconds=80)
        end_time = datetime.datetime.utcnow().replace(microsecond=0, second=0) - time_delay
        start_time = end_time - datetime.timedelta(seconds=history if history > 0 else interval)
        result = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric,
            Dimensions=dimensions,
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Statistics=[statistic, ],
            Period=interval)

        # We use only the last datapoint from list
        # Return -1 if there are no datapoints
        if len(result["Datapoints"]) > 0:
            ret_val = result["Datapoints"][len(result["Datapoints"]) - 1][statistic]
        else:
            ret_val = -1
        if self.debug:
            print(result)

        # Some CW metrics are returned as float rather than an integer.
        # This can be a problem, because RDS instances can be huge
        # and overflow Zabbix DB floating point data type
        if metric in ["FreeStorageSpace", "BytesUsedForCache", "FreeableMemory", "SwapUsage", "Evictions", "CurrConnections"]:
            ret_val = int(ret_val)
        return ret_val

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gets metrics from CW")

    # Metric specifications
    parser.add_argument("--interval", dest="interval",
                        help="Refresh interval",
                        required=True, type=int)
    parser.add_argument("--metric", dest="metric",
                        help="Name of metric",
                        required=True, type=str)
    parser.add_argument("--namespace", dest="namespace",
                        help="Metric namespace",
                        required=True, type=str)
    parser.add_argument("--statistic", dest="statistic",
                        help="Type of statistic",
                        required=True, type=str)
    parser.add_argument("--dimension", dest="dimension",
                        help="Dimension(s)",
                        required=True, type=str)

    # Account specific
    parser.add_argument("--region", dest="region",
                        help="Instance region",
                        required=True, type=str)
    parser.add_argument("--account", dest="account",
                        help="Instance account",
                        required=True, type=str)

    # Authentication
    parser.add_argument("--assume-role", dest="assume_role",
                        help="Instance role to assume",
                        default=os.environ.get('AWS_ROLE_ARN', None),
                        required=False, type=str)

    # Details
    parser.add_argument("--history", dest="history",
                        help="Amount of seconds to fetch history, latest datapoint will be chosen",
                        required=False, default=0)
    parser.add_argument("--debug", dest="debug",
                        action="store_true", help="Debug flag",
                        required=False)
    args = parser.parse_args()

    # AWS requires dimension to be dict like:
    # { "Name": dimension_name, "Value" dimension_value }
    dimensions = list()
    for dimension in args.dimension.split(","):
        instance = dimension.split("=")
        dimensions.append(dict(zip(("Name", "Value"), instance)))

    checker = Checker(
        account=args.account,
        service="cloudwatch",
        region=args.region,
        # Optional authentication
        assume_role=args.assume_role
    )
    checker.debug = args.debug

    print(checker.get_metric(interval=args.interval,
                             metric=args.metric,
                             namespace=args.namespace,
                             statistic=args.statistic,
                             history=args.history,
                             dimensions=dimensions))
