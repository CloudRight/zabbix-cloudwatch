#!/usr/bin/env python3
import argparse
import importlib
import os

if __name__ == "__main__":
    # Using CLI argument parser to save brain cells
    # if we need to add some arg down the road
    parser = argparse.ArgumentParser(
        description="AWS Service instances Zabbix discovery script")
    parser.add_argument("--service", dest="service",
                        help="Service to discover instances in",
                        required=True, type=str)
    # Account specific
    parser.add_argument("--region", dest="region",
                        help="AWS region for discovery",
                        required=True, type=str)
    parser.add_argument("--account", dest="account",
                        help="AWS account for discovery",
                        required=True, type=str)
    # Authentication
    parser.add_argument("--assume-role", dest="assume_role",
                        help="Instance role to assume",
                        default=os.environ.get('AWS_ROLE_ARN', None),
                        required=False, type=str)
    # Optional args
    parser.add_argument("--args", dest="args", default="",
                        help="Optional args for discovery modules",
                        required=False, type=str, nargs="+")
    parser.add_argument("--debug", dest="debug",
                        action="store_true", help="Debug flag",
                        required=False)
    args = parser.parse_args()

    # Tricky part is to dynamically import ONLY one module
    # for the service that was requested by CLI argument
    discovery_module = importlib.import_module(".{}".format(args.service),
                                               "discovery")

    if args.service in ["s3", "lambda"]:
        service = "cloudwatch"
    else:
        service = args.service

    # Create instance of discoverer from this module and run actual discovery
    d = discovery_module.Discoverer(
        account=args.account,
        service=service,
        region=args.region,
        # Optional authentication
        assume_role=args.assume_role
    )
    print(d.get_instances(*args.args))
