from prefect import task
from etl.utilities.sql_queries import \
    covid_data_filtered_by_tokyo
from etl.utilities.db_utility import \
    execute_sql_query_and_get_result_as_df, \
    upload_df_to_table


@task
def create_table_tokyo_covid_by_prefecture():
    """
    Creates table that contains covid data
    for Tokyo prefecture.
    :return:
    """
    result_df = execute_sql_query_and_get_result_as_df(
        covid_data_filtered_by_tokyo
    )

    upload_df_to_table(df=result_df,
                       table_name='dim_tokyo_covid_by_prefecture')

