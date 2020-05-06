#!/usr/bin/env python2
import argparse
import importlib


if __name__ == "__main__":
    # Using CLI argument parser to save brain cells
    # if we need to add some arg down the road
    parser = argparse.ArgumentParser(
                description="AWS Service instances Zabbix discovery script")
    parser.add_argument("--service", dest="service",
                        help="Service to discover instances in",
                        required=True, type=str)
    parser.add_argument("--region", dest="region",
                        help="AWS region for discovery",
                        required=True, type=str)
    parser.add_argument("--account", dest="account",
                        help="AWS account for discovery",
                        required=True, type=str)
    parser.add_argument("--args", dest="args", default="",
                        help="Optional args for discovery modules",
                        required=False, type=str, nargs="+")
    args = parser.parse_args()

    # Tricky part is to dynamically import ONLY one module
    # for the serice that was requested by CLI argument
    discovery_module = importlib.import_module(".{}".format(args.service),
                                               "discovery")

    # Create instance of discoverer from this module and run actual discovery
    d = discovery_module.Discoverer(args.account,
                                    args.service, args.region)
    print d.get_instances(*args.args)
