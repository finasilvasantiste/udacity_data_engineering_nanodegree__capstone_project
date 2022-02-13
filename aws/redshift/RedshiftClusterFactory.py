from aws.redshift.RedshiftCluster import RedshiftCluster


class RedshiftClusterFactory:
    """
    Represents a Redshift Cluster factory.
    """

    @staticmethod
    def create_redshift_cluster():
        """
        Creates all redshift cluster ander
        necessary aws redshift resources.
        Prints out cluster details at the end.
        :return:
        """
        redshift_cluster = RedshiftCluster()
        redshift_cluster.create_all_resources()
        RedshiftCluster.describe_cluster()

    @staticmethod
    def delete_redshift_cluster():
        """
        Deletes redshift cluster and resources.
        :return:
        """
        redshift_cluster = RedshiftCluster()
        redshift_cluster.delete_all_resources()
