from prefect import task
import configparser
import json
from etl.db_utility import execute_sql_query


config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))


def load_iam_role_arn():
    """
    Loads iam role arn.
    :return:
    """
    # Opening JSON file
    f = open('aws_role_arn.json', )

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    return data['iam_role_arn']


@task
def create_calendar_staging_table():
    """
    Creates staging table for calendar data.
    :return:
    """
    sql_query_create_table = ("""
CREATE TABLE IF NOT EXISTS tokyo_airbnb_calendar (
   listing_id NUMERIC PRIMARY KEY,
   date TIMESTAMP,
   available BOOLEAN,
   price VARCHAR,
   adjusted_price VARCHAR,
   minimum_nights NUMERIC,
   maximum_nights NUMERIC
);
""")

    execute_sql_query(sql_query_create_table)


@task
def load_calendar_data_into_staging_table():
    """
    Load calendar data into calendar staging table.
    :return:
    """
    iam_role_arn = load_iam_role_arn()
    file_path = config.get('S3', 'CALENDAR_DATA')
    region = config.get('AWS_CREDS_ADMIN', 'AWS_REGION')

    sql_query_copy_data = """
    COPY tokyo_airbnb_calendar 
    FROM '{}' 
    credentials 'aws_iam_role={}' 
    CSV IGNOREHEADER 1 compupdate off region '{}';
    """.format(file_path, iam_role_arn, region)

    execute_sql_query(sql_query_copy_data)

