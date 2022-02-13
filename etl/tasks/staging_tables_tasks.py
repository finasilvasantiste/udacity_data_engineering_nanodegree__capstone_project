from prefect import task
import configparser
import json
from etl.utilities.db_utility import execute_sql_query, \
    execute_sql_query_and_get_result
from etl.utilities.sql_queries import create_staging_calendar_table, \
    copy_calendar_data_staging_table, \
    drop_staging_calendar_table, \
    drop_staging_covid_table, \
    create_staging_covid_table, \
    copy_covid_data_staging_table, \
    count_rows

config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))


def load_iam_role_arn():
    """
    Loads iam role arn from json file.
    (Json file got populated during redshift
    cluster creation.)
    :return: iam role arn string
    """
    f = open('aws_role_arn.json', )
    data = json.load(f)
    f.close()

    return data['iam_role_arn']


@task
def drop_calendar_staging_table():
    """
    Drops staging table for calendar data
    if it already exists.
    :return:
    """
    execute_sql_query(drop_staging_calendar_table)


@task
def create_calendar_staging_table():
    """
    Creates staging table for calendar data.
    :return:
    """
    execute_sql_query(create_staging_calendar_table)


@task
def load_calendar_data_into_staging_table():
    """
    Load calendar data into calendar staging table.
    :return:
    """
    iam_role_arn = load_iam_role_arn()
    file_path = config.get('S3', 'CALENDAR_DATA')
    region = config.get('AWS_CREDS_ADMIN', 'AWS_REGION')

    execute_sql_query(copy_calendar_data_staging_table.format(
        file_path, iam_role_arn, region
    ))


@task
def drop_covid_staging_table():
    """
    Drops staging table for covid data
    if it already exists.
    :return:
    """
    execute_sql_query(drop_staging_covid_table)


@task
def create_covid_staging_table():
    """
    Creates covid table for calendar data.
    :return:
    """
    execute_sql_query(create_staging_covid_table)


@task
def load_covid_data_into_staging_table():
    """
    Load covid data into calendar staging table.
    :return:
    """
    iam_role_arn = load_iam_role_arn()
    file_path = config.get('S3', 'COVID_JPN_DATA')
    region = config.get('AWS_CREDS_ADMIN', 'AWS_REGION')

    execute_sql_query(copy_covid_data_staging_table.format(
        file_path, iam_role_arn, region
    ))


@task
def run_quality_checks_for_staging_tables():
    """
    Runs quality checks on existing staging tables.
    The first check confirms the tables are not empty.
    :return:
    """
    # count rows check
    calendar_staging_table = 'tokyo_airbnb_calendar'
    covid_staging_table = 'covid_japan_by_prefecture'

    calender_count = int(execute_sql_query_and_get_result(
            count_rows.format(calendar_staging_table)
        )[0][0])
    covid_count = int(execute_sql_query_and_get_result(
            count_rows.format(covid_staging_table)
        )[0][0])

    if calender_count <= 0 or covid_count <= 0:
        raise Exception("One or more staging tables are empty.")
