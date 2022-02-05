import configparser
from aws.AWSClient import AWSClient
from aws.AWSResource import AWSResource
import pandas as pd
import json
import time
import json

config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))


class RedshiftCluster:
    """ Represents a redshift cluster."""
    cluster_identifier = config.get('REDSHIFT_CLUSTER', 'CLUSTER_IDENTIFIER')

    def __init__(self):
        self.user_name = config.get('REDSHIFT_CLUSTER', 'USER_NAME')
        self.password = config.get('REDSHIFT_CLUSTER', 'PASSWORD')
        self.cluster_identifier = config.get('REDSHIFT_CLUSTER', 'CLUSTER_IDENTIFIER')
        self.cluster_type = 'multi-node'
        self.node_type = 'dc2.Large'
        self.number_of_nodes = 4
        self.db_name = config.get('REDSHIFT_CLUSTER', 'DB_NAME')
        self.iam_role_name = config.get('REDSHIFT_CLUSTER', 'IAM_ROLE_NAME')
        self.iam_role_arn = None

    def create_iam_role(self):
        """
        Creates IAM role for redshift cluster to access S3.
        :return:
        """
        iam_client = AWSClient(client_name='iam').client

        try:
            print('+++++ Creating IAM Role... +++++')

            iam_client.create_role(
                Path='/',
                RoleName=self.iam_role_name,
                Description = "Allows Redshift clusters to call AWS services on your behalf.",
                AssumeRolePolicyDocument=json.dumps(
                    {'Statement': [{'Action': 'sts:AssumeRole',
                                    'Effect': 'Allow',
                                    'Principal': {'Service': 'redshift.amazonaws.com'}}],
                     'Version': '2012-10-17'})
            )
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

        try:
            print('+++++ Attaching IAM Role Policy... +++++')

            iam_client.attach_role_policy(
                RoleName=self.iam_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess')
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

        try:
            print('+++++ Saving IAM Role ARN to file... +++++')

            self.iam_role_arn = iam_client.get_role(RoleName=self.iam_role_name)['Role']['Arn']
            RedshiftCluster.save_iam_role_arn_to_file(self.iam_role_arn)
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    @staticmethod
    def save_iam_role_arn_to_file(arn):
        """
        Saves iam role arn to file for future use.
        :param arn: iam role arn
        :return:
        """
        dictionary = {
            "iam_role_arn": arn
        }

        with open("aws_role_arn.json", "w") as outfile:
            json.dump(dictionary, outfile)

    def delete_iam_role(self):
        """
        Deletes IAM role for redshift cluster to access S3.
        :return:
        """
        iam_client = AWSClient(client_name='iam').client

        try:
            print('+++++ Deleting IAM Role ARN... +++++')

            iam_client.detach_role_policy(RoleName=self.iam_role_name,
                                          PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
                                          )
            iam_client.delete_role(RoleName=self.iam_role_name)
            self.iam_role_arn = None
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    def add_inbound_rule(self):
        """
        Add inbound rule for Redshift.
        :return:
        """
        ec2 = AWSResource(resource_name='ec2').resource
        vpc_id = RedshiftCluster.get_cluster_vpc_id_from_cloud()
        port = RedshiftCluster.get_cluster_port_from_cloud()

        try:
            print('+++++ Adding Redshift inbound rule to security group... +++++')
            vpc = ec2.Vpc(id=vpc_id)
            defaultSg = list(vpc.security_groups.all())[-1]  # Using default group.
            print(defaultSg)
            defaultSg.authorize_ingress(
                GroupName=defaultSg.group_name,
                CidrIp='0.0.0.0/0',
                IpProtocol='TCP',
                FromPort=int(port),
                ToPort=int(port)
            )
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    def create_all_resources(self):
        """
        Creates all necessary Redshift resources.
        :return:
        """
        self.create_iam_role()
        self.create_cluster()
        self.add_inbound_rule()

    def create_cluster(self):
        """
        Creates redshift cluster.
        :return:
        """
        redshift_client = AWSClient(client_name='redshift').client

        try:
            print('+++++ Creating cluster {}... +++++'.format(self.cluster_identifier))

            redshift_client.create_cluster(ClusterIdentifier=self.cluster_identifier,
                                           ClusterType=self.cluster_type,
                                           NodeType=self.node_type,
                                           MasterUsername=self.user_name,
                                           MasterUserPassword=self.password,
                                           NumberOfNodes=self.number_of_nodes,
                                           IamRoles=[self.iam_role_arn],
                                           DBName=self.db_name,
                                           # This is to make it work for the airflow project,
                                           # which requires us-west-2 region.
                                           # (I went into the console and created this subnet in that region.)
                                           ClusterSubnetGroupName='cluster-subnet-group-1'
                                           )
            RedshiftCluster.wait_for_cluster_availability()
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    def delete_all_resources(self):
        """
        Delete all resources.
        :return:
        """
        self.delete_iam_role()
        self.delete_cluster()

    def delete_cluster(self):
        """
        Deletes redshift cluster.
        :return:
        """
        redshift_client = AWSClient(client_name='redshift').client

        try:
            print('+++++ Deleteting cluster {}... +++++'.format(self.cluster_identifier))

            redshift_client.delete_cluster(ClusterIdentifier=self.cluster_identifier,
                                           SkipFinalClusterSnapshot=True)
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    @staticmethod
    def get_cluster_description():
        """
        Returns cluster description. Queries aws to get the arn.
        :return:
        """
        redshift_client = AWSClient(client_name='redshift').client
        cluster_description = redshift_client.describe_clusters(ClusterIdentifier=RedshiftCluster.cluster_identifier)['Clusters'][0]

        return cluster_description

    @staticmethod
    def get_cluster_status():
        """
        Returns cluster status.
        :return: string containing cluster status
        """
        cluster_description = RedshiftCluster.get_cluster_description()
        cluster_status = cluster_description['ClusterStatus']

        return cluster_status

    @staticmethod
    def get_cluster_vpc_id_from_cloud():
        """
        Returns cluster vpc id. Queries aws to get the information.
        :return:
        """
        cluster_description = RedshiftCluster.get_cluster_description()
        vpc_id = cluster_description['VpcId']

        return vpc_id

    @staticmethod
    def get_cluster_address_from_cloud():
        """
        Returns cluster address. Queries aws to get the information.
        :return:
        """
        cluster_description = RedshiftCluster.get_cluster_description()
        arn = cluster_description['Endpoint']['Address']

        return arn

    @staticmethod
    def get_cluster_port_from_cloud():
        """
        Returns cluster port. Queries aws to get the information.
        :return:
        """
        cluster_description = RedshiftCluster.get_cluster_description()
        port = cluster_description['Endpoint']['Port']

        return port

    @staticmethod
    def is_available():
        """
        Returns whether cluster status is available.
        :return: boolean
        """
        cluster_status = RedshiftCluster.get_cluster_status()

        return cluster_status == 'available'

    @staticmethod
    def wait_for_cluster_availability():
        """
        Waits until cluster is available.
        :return:
        """
        while not RedshiftCluster.is_available():
            print('+++++ Cluster is not available yet. '
                  'Waiting 10 seconds before checking the cluster status again. +++++')

            time.sleep(10)

        print('+++++ Cluster is available. +++++')

    @staticmethod
    def describe_cluster():
        """
        Describes redshift cluster.
        :return:
        """
        try:
            print('+++++ Describing cluster: +++++')
            cluster_description = RedshiftCluster.get_cluster_description()
            print(RedshiftCluster.prettyRedshiftProps(cluster_description))
        except Exception as e:
            print('+++++ Threw Exception +++++')
            print(e)

    # copy-pasted this handy method from a jupyter notebook used in the lecture.
    @staticmethod
    def prettyRedshiftProps(props):
        """
        Formats given props in a way that is easier to read.
        :param props: data to format
        :return: df with formatted data
        """
        pd.set_option('display.max_colwidth', None)
        keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint",
                      "NumberOfNodes", 'VpcId']
        x = [(k, v) for k, v in props.items() if k in keysToShow]
        return pd.DataFrame(data=x, columns=["Key", "Value"])
