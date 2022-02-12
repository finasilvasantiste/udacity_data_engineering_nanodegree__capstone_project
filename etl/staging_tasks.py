from prefect import task
import prefect
from aws.s3 import print_s3_bucket_content
import configparser
import psycopg2
import redshift_connector
import json


config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))


# CONVENIENCE METHOD
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
    db_name = config.get('REDSHIFT_CLUSTER', 'DB_NAME')
    db_user_name = config.get('REDSHIFT_CLUSTER', 'USER_NAME')
    password = config.get('REDSHIFT_CLUSTER', 'PASSWORD')
    host = config.get('REDSHIFT_CLUSTER', 'HOST')

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

    print(sql_query_create_table)

    conn = redshift_connector.connect(
        host=host,
        database=db_name,
        user=db_user_name,
        password=password
    )

    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(sql_query_create_table)
    conn.commit()


@task
def load_calendar_data_into_staging_table():
    iam_role_arn = load_iam_role_arn()
    file_path = config.get('S3', 'CALENDAR_DATA')

    db_name = config.get('REDSHIFT_CLUSTER', 'DB_NAME')
    db_user_name = config.get('REDSHIFT_CLUSTER', 'USER_NAME')
    password = config.get('REDSHIFT_CLUSTER', 'PASSWORD')
    host = config.get('REDSHIFT_CLUSTER', 'HOST')
    user = config.get('AWS_CREDS_ADMIN', 'USER_NAME')
    cluster_identifier = config.get('REDSHIFT_CLUSTER', 'CLUSTER_IDENTIFIER')
    access_key_id = config.get('AWS_CREDS_ADMIN', 'AWS_ACCESS_KEY_ID')
    secret_access_key = config.get('AWS_CREDS_ADMIN', 'AWS_SECRET_ACCESS_KEY')
    region = config.get('AWS_CREDS_ADMIN', 'AWS_REGION')

    sql_query_copy_data = """
    COPY tokyo_airbnb_calendar 
    FROM '{}' 
    credentials 'aws_iam_role={}' 
    CSV IGNOREHEADER 1 compupdate off region '{}';
    """.format(file_path, iam_role_arn, region)

    print(sql_query_copy_data)

    conn = redshift_connector.connect(
        host=host,
        database=db_name,
        user=db_user_name,
        password=password
    )

    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(sql_query_copy_data)
    conn.commit()


