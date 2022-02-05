from aws.RedshiftCluster import RedshiftCluster


def create_aws_redshift_resources():
    """
    Creates all necessary aws redshift resources.
    Prints out cluster details at the end.
    :return:
    """
    redshift_cluster = RedshiftCluster()
    redshift_cluster.create_all_resources()
    RedshiftCluster.describe_cluster()


if __name__ == "__main__":
    create_aws_redshift_resources()
