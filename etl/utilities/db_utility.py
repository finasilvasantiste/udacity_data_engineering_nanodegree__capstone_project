import redshift_connector
import configparser
import pandas as pd
from sqlalchemy import create_engine


config = configparser.ConfigParser()
config.read_file((open(r'dwh.cfg')))

db_name = config.get('REDSHIFT_CLUSTER', 'DB_NAME')
db_user_name = config.get('REDSHIFT_CLUSTER', 'USER_NAME')
password = config.get('REDSHIFT_CLUSTER', 'PASSWORD')
host = config.get('REDSHIFT_CLUSTER', 'HOST')


def execute_sql_query(sql_query):
    """
    Creates a connection to db on redshift cluster
    and executes given sql query.
    :param sql_query: sql query to execute
    :return:
    """
    print('++++++ QUERY TO EXECUTE ++++++')
    print(sql_query)

    conn = redshift_connector.connect(
        host=host,
        database=db_name,
        user=db_user_name,
        password=password
    )

    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    conn.close()


def execute_sql_query_and_get_result(sql_query):
    """
    Creates a connection to db on redshift cluster,
    executes given sql query and returns result.
    :param sql_query: sql query to execute
    :return: query result
    """
    print('++++++ QUERY TO EXECUTE ++++++')
    print(sql_query)

    conn = redshift_connector.connect(
        host=host,
        database=db_name,
        user=db_user_name,
        password=password
    )

    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()

    result: tuple = cursor.fetchall()

    print('++++++ RESULT ++++++')
    print(result)

    conn.close()

    return result


def execute_sql_query_and_get_result_as_df(sql_query):
    """
    Creates a connection to db on redshift cluster,
    executes given sql query and returns result as df.
    :param sql_query: sql query to execute
    :return: query result
    """
    print('++++++ QUERY TO EXECUTE ++++++')
    print(sql_query)

    conn = redshift_connector.connect(
        host=host,
        database=db_name,
        user=db_user_name,
        password=password
    )

    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    result: pd.DataFrame = cursor.fetch_dataframe()

    print('++++++ RESULT ++++++')
    print(result)

    conn.close()

    return result


def upload_df_to_table(df, table_name):
    """
    Uploads given dataframe to db.
    If a table with given name already exists
    it will be replaced.
    :param df: df to upload
    :param table_name: table name to use
    :return:
    """
    print("++++++ UPLOADING DF TO TABLE '{}' ++++++".format(table_name))

    conn = create_engine('postgresql://{}:{}@{}:5439/{}'.format(
        db_user_name, password, host, db_name
    ))

    df.to_sql(table_name, conn, index=False, if_exists='replace')
