import redshift_connector
import configparser

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
