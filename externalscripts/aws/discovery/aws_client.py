import boto3


class AWSClient(object):
    """Basic object for AWS services discovery"""

    def __init__(self, account, service, region, assume_role=None):
        """Initializes Boto3 client for specified service"""

        # Deal with assuming roles
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_session_token = None

        if assume_role is not None:
            # Deal with STS
            client = boto3.client("sts")

            response = client.assume_role(
                RoleArn=assume_role,
                RoleSessionName=__name__,
            )

            self.aws_access_key_id = response["Credentials"]["AccessKeyId"]
            self.aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
            self.aws_session_token = response["Credentials"]["SessionToken"]

        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
        )

        self.client = session.client(service, region_name=region)
        self.region = region
