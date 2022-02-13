from prefect import task


@task
def create_table_tokyo_covid_by_prefecture():
    """
    Creates the table that contains covid data
    for Tokyo prefecture.
    :return:
    """
    pass