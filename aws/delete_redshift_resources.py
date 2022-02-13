from aws.redshift.RedshiftClusterFactory import RedshiftClusterFactory


def delete_aws_redshift_resources():
    """
    Deletes redshift cluster and redshift resources.
    :return:
    """
    RedshiftClusterFactory.delete_redshift_cluster()


if __name__ == "__main__":
    delete_aws_redshift_resources()
