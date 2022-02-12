from prefect import Flow
from etl.staging_tasks import create_calendar_staging_table,\
    load_calendar_data_into_staging_table, \
    drop_calendar_staging_table, \
    drop_covid_staging_table, \
    create_covid_staging_table, \
    load_covid_data_into_staging_table

# CREATE FLOW
flow = Flow('ETL Pipeline')

# POPULATE STAGING TABLES

# AIRBNB LISTINGS CALENDAR DATA
flow.set_dependencies(
    task=drop_calendar_staging_table)

flow.set_dependencies(
    task=create_calendar_staging_table,
    upstream_tasks=[drop_calendar_staging_table])

flow.set_dependencies(
    task=load_calendar_data_into_staging_table,
    upstream_tasks=[create_calendar_staging_table])

# COVID JAPAN DATA
flow.set_dependencies(
    task=drop_covid_staging_table)

flow.set_dependencies(
    task=create_covid_staging_table,
    upstream_tasks=[drop_covid_staging_table])

flow.set_dependencies(
    task=load_covid_data_into_staging_table,
    upstream_tasks=[create_covid_staging_table])
