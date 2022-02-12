from prefect import task
import prefect
from aws.s3 import print_s3_bucket_content
import configparser
import psycopg2
import redshift_connector


config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))


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

    # Connects to Redshift cluster using AWS credentials
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
    iam_role_arn = config.get('REDSHIFT_CLUSTER', 'ADMIN_USER_ARN')
    db_name = config.get('REDSHIFT_CLUSTER', 'DB_NAME')
    user_name = config.get('REDSHIFT_CLUSTER', 'USER_NAME')
    password = config.get('REDSHIFT_CLUSTER', 'PASSWORD')
    host = config.get('REDSHIFT_CLUSTER', 'HOST')
    file_path = config.get('S3', 'CALENDAR_DATA')

    copy_sql_query = """
    copy tokyo_airbnb_calendar
    from '{}'
    iam_role '{}'
    Csv NOLOAD
    IGNOREHEADER 1;
    """.format(file_path, iam_role_arn)

    print(copy_sql_query)

    try:
        # Connects to Redshift cluster using AWS credentials
        conn = redshift_connector.connect(
            host=host,
            database=db_name,
            user=user_name,
            password=password
        )

        cursor: redshift_connector.Cursor = conn.cursor()
        cursor.execute(copy_sql_query)
        conn.close()

    except Exception as e:
        print(e)
