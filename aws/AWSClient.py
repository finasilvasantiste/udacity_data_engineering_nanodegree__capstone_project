import boto3
from aws.AWSEntity import AWSEntity


class AWSClient(AWSEntity):
    """ Represents an aws client. """

    def __init__(self, client_name):
        super().__init__()
        session = self.get_boto3_session()
        self.client = session.client(client_name)

    def get_boto3_session(self):
        """
        Returns authenticated boto3 session.
        :return:
        """
        session = boto3.Session(aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key,
                                region_name=self.aws_region)

        return session
