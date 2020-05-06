#!/usr/bin/env python2
import boto3


class AWSClient(object):
    "Basic object for AWS services discovery"
    def __init__(self, account, service, region):
        "Initializes Boto3 client for specified service"
        self.client = boto3.client(
            service,
            region_name=region)
        self.region = region
