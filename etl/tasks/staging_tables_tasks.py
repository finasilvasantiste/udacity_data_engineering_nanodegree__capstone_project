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
    count_rows, distinct_count_rows
from aws.entities.AWSClient import AWSClient
import pandas as pd
import io


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
    file_path = config.get('S3', 'CALENDAR_DATA_FULL_PATH')
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
    file_path = config.get('S3', 'COVID_JPN_DATA_FULL_PATH')
    region = config.get('AWS_CREDS_ADMIN', 'AWS_REGION')

    execute_sql_query(copy_covid_data_staging_table.format(
        file_path, iam_role_arn, region
    ))


def check_staging_tables_row_count_match_file():
    """
    Checks if staging tables row count matches
    corresponding file row count. Raises an exception
    if it doesn't match for at least one table.
    :return:
    """
    bucket_name = config.get('S3', 'BUCKET_NAME')
    data_to_download = [{'s3_key': config.get('S3', 'CALENDAR_DATA_KEY'), 'data_name': 'calendar_data'},
                        {'s3_key': config.get('S3', 'COVID_JPN_DATA_KEY'), 'data_name': 'covid_data'}]
    s3 = AWSClient(client_name='s3').client

    dfs = {}

    # Download files into dfs.
    for data in data_to_download:
        obj = s3.get_object(Bucket=bucket_name, Key=data['s3_key'])
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')

        dfs[data['data_name']] = df

    tables_to_check = [{'table_name': 'tokyo_airbnb_calendar', 'data_name': 'calendar_data'},
                       {'table_name': 'covid_japan_by_prefecture', 'data_name': 'covid_data'}]
    count_results = {}

    # Get staging tables row count.
    for table in tables_to_check:
        count = int(execute_sql_query_and_get_result(
            count_rows.format(table['table_name'])
        )[0][0])

        count_results[table['data_name']] = count

    data_names = ['calendar_data', 'covid_data']

    # Calculate difference between file row count
    # staging table row count.
    for data_name in data_names:
        data_difference = abs(len(dfs[data_name]) - count_results[data_name])

        if data_difference > 0:
            raise Exception("Staging table row count does not match file "
                            "row count for at least one table.")


def check_staging_tables_not_empty():
    """
    Checks if staging tables are not empty. Raises an exception
    if at least one staging table is empty.
    :return:
    """
    table_names = ['tokyo_airbnb_calendar', 'covid_japan_by_prefecture']

    # Get staging tables row count.
    for table in table_names:
        count = int(execute_sql_query_and_get_result(
            count_rows.format(table)
        )[0][0])

        if count <= 0:
            raise Exception("At least one staging table is empty.")


def remove_duplicates_from_staging_tables():
    """
    Removes duplicate rows from staging tables.
    :return:
    """
    table_names = ['tokyo_airbnb_calendar', 'covid_japan_by_prefecture']

    for table_name in table_names:
        overall_count = int(execute_sql_query_and_get_result(
            count_rows.format(table_name)
        )[0][0])

        distinct_count = int(execute_sql_query_and_get_result(
            distinct_count_rows.format(table_name)
        )[0][0])

        difference = abs(overall_count - distinct_count)

        if difference > 0:
            # I ran some manual checks on the redshift cluster query editor
            # and noticed that the data doesn't have any duplicates.
            # I'm adding this exception so that in case that changes
            # the ETL pipeline fails.
            raise Exception("At least one staging table has duplicate rows. "
                            "Cleanup of duplicate rows is needed.")


@task
def run_quality_checks_for_staging_tables():
    """
    Runs quality checks on existing staging tables.
    The checks to run:
    - confirm the staging tables row count
    matches the files' row count.
    - confirm staging tables are not empty.
    - remove duplicates rows from staging tables.
    :return:
    """
    check_staging_tables_row_count_match_file()
    check_staging_tables_not_empty()
    remove_duplicates_from_staging_tables()
