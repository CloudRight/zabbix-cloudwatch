#!/usr/bin/env python2
import boto3


class AWSClient(object):
    "Basic object for AWS services discovery"
    def __init__(self, profile, service, region):
        "Initializes Boto3 client for specified service"
        session = boto3.Session(profile_name=profile)
        self.client = session.client(
            service,
            region_name=region)
        self.region = region
