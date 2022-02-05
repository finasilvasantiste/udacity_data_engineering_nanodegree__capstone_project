import boto3
from aws.AWSEntity import AWSEntity


class AWSResource(AWSEntity):
    """ Represents an aws client. """

    def __init__(self, resource_name):
        super().__init__()
        self.resource = boto3.resource(resource_name,
                                       region_name=self.aws_region,
                                       aws_access_key_id=self.aws_access_key_id,
                                       aws_secret_access_key=self.aws_secret_access_key
                                       )

