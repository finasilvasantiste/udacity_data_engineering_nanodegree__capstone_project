from aws.redshift.RedshiftClusterFactory import RedshiftClusterFactory


def create_aws_redshift_resources():
    """
    Creates redshift cluster and
    all necessary aws redshift resources.
    Prints out cluster details at the end.
    :return:
    """
    RedshiftClusterFactory.create_redshift_cluster()


if __name__ == "__main__":
    create_aws_redshift_resources()
