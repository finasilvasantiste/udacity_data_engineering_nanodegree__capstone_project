import configparser


class AWSEntity:
    """ Represents an aws entity. """

    aws_users = {'admin': 'AWS_CREDS_ADMIN'}

    def __init__(self):
        aws_access_key_id, aws_secret_access_key, aws_region = self.get_aws_credentials()

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

    def get_aws_credentials(self):
        """
        Returns aws credentials for admin user.
        :return: three strings
        """
        config = configparser.ConfigParser()
        config.read_file((open(r'dwh.cfg')))
        aws_user = self.aws_users['admin']

        aws_access_key_id = config.get(aws_user, 'AWS_ACCESS_KEY_ID')
        aws_secret_access_key = config.get(aws_user, 'AWS_SECRET_ACCESS_KEY')
        aws_region = config.get(aws_user, 'AWS_REGION')

        return aws_access_key_id, aws_secret_access_key, aws_region
