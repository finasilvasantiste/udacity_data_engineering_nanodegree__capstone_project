from aws.RedshiftCluster import RedshiftCluster


def delete_aws_redshift_resources():
    """
    Deletes all newly created aws redshift resources.
    :return:
    """
    redshift_cluster = RedshiftCluster()
    redshift_cluster.delete_all_resources()


if __name__ == "__main__":
    delete_aws_redshift_resources()
