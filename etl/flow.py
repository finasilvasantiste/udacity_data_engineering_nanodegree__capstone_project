from prefect import Flow
from etl.staging_tasks import create_calendar_staging_table,\
    load_calendar_data_into_staging_table, \
    drop_calendar_staging_table, \
    drop_covid_staging_table, \
    create_covid_staging_table, \
    load_covid_data_into_staging_table


with Flow("airbnb-tokyo-covid-data") as flow:
    # 1) POPULATE STAGING TABLES

    # AIRBNB LISTINGS CALENDAR DATA
    # drop_calendar_staging_table()
    # create_calendar_staging_table()
    # load_calendar_data_into_staging_table()

    # COVID JAPAN DATA
    drop_covid_staging_table()
    create_covid_staging_table()
    load_covid_data_into_staging_table()
