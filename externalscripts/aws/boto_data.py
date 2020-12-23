#!/usr/bin/env python3
import argparse
from functools import reduce
from os import environ
import datetime
from json import dumps

from prodict import Prodict

from discovery.aws_client import AWSClient


def default_ts(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return int(o.strftime('%s'))

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def rgetattr(obj, path, default=None):
    try:
        return reduce(getattr, path.split(), obj)
    except AttributeError:
        return default


class Retriever(AWSClient):
    def exec_function(self, function, filter, arguments):
        # todo: check if we can obtain which arguments are SET and which one's are REQUIRED by the function
        data = getattr(self.client, function)(**arguments)

        # Return unfiltered data
        if not filter:
            return data

        # Apply filtering on the data to retrieve the specific information
        props = Prodict.from_dict(data)
        value = rgetattr(props, filter.replace('.', ' '))

        # Convert timestamps into Unix timestamps since its easier for Zabbix to work with
        if isinstance(value, datetime.datetime):
            value = value.strftime('%s')

        return value

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gets details from Boto")

    # Mandatory
    parser.add_argument("--service", dest="service",
                        help="Type of service",
                        required=True, type=str)
    parser.add_argument("--function", dest="function",
                        help="Function to call in Boto",
                        required=True, type=str)
    parser.add_argument('--filter', dest="filter",
                        help="Output filter", default=False,
                        type=str)
    parser.add_argument('--args', dest="args",
                        help="Arguments", nargs='*',
                        action=ParseKwargs)

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
                        default=environ.get('AWS_ROLE_ARN', None),
                        required=False, type=str)

    # Misc
    parser.add_argument("--debug", dest="debug",
                        action="store_true", help="Debug flag",
                        required=False)
    args = parser.parse_args()

    # Instantiate the AWS Client with required parameters
    retriever = Retriever(
        account=args.account,
        service=args.service,
        region=args.region,
        # Optional authentication
        assume_role=args.assume_role
    )
    retriever.debug = args.debug

    if args.filter:
        print(retriever.exec_function(args.function, args.filter, args.args))
    else:
        print(dumps(retriever.exec_function(args.function, args.filter, args.args), sort_keys=True, default=default_ts))
