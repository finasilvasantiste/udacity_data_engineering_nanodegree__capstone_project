from prefect import task
from etl.utilities.sql_queries import \
    covid_data_filtered_by_tokyo, \
    aggr_tokyo_listings_availability, \
    tokyo_listings_availability_and_covid_rates
from etl.utilities.db_utility import \
    execute_sql_query_and_get_result_as_df, \
    upload_df_to_table
import pandas as pd


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

    result_df[["tested_total", "tested_positive"]] = result_df[
        ["tested_total", "tested_positive"]].apply(pd.to_numeric)

    upload_df_to_table(df=result_df,
                       table_name='dim_tokyo_covid_by_prefecture')


@task
def create_table_tokyo_aggr_listings_availability():
    """
    Creates table that contains count of total listings
    (both available and unavailable listings) and count of only
    available listings by dates for listings in Tokyo.
    :return:
    """
    result_df = execute_sql_query_and_get_result_as_df(
        aggr_tokyo_listings_availability
    )

    result_df[["listings_total_count", "listings_available_count"]] = result_df[
        ["listings_total_count", "listings_available_count"]].apply(pd.to_numeric)

    upload_df_to_table(df=result_df,
                       table_name='dim_tokyo_aggregated_listings_availability')


@task
def create_table_tokyo_listings_availability_and_covid_rates():
    """
    Creates table that contains Tokyo listings availability
    rate and covid rates by date.
    :return:
    """
    result_df = execute_sql_query_and_get_result_as_df(
        tokyo_listings_availability_and_covid_rates
    )

    # upload_df_to_table(df=result_df,
    #                    table_name='dim_tokyo_aggregated_listings_availability')