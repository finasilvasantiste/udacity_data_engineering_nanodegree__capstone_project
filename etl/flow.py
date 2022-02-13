from prefect import Flow
from etl.tasks.staging_tables_tasks import \
    create_calendar_staging_table,\
    load_calendar_data_into_staging_table, \
    drop_calendar_staging_table, \
    drop_covid_staging_table, \
    create_covid_staging_table, \
    load_covid_data_into_staging_table, \
    run_quality_checks_for_staging_tables
from etl.tasks.new_tables_tasks import \
    create_table_tokyo_covid_by_prefecture, \
    create_table_tokyo_aggr_listings_availability, \
    create_table_tokyo_listings_availability_and_covid_rates


# CREATE FLOW/ETL PIPELINE.
flow = Flow('ETL Pipeline')

# 1) POPULATE STAGING TABLES.
# AIRBNB LISTINGS CALENDAR DATA.
flow.set_dependencies(
    task=drop_calendar_staging_table)

flow.set_dependencies(
    task=create_calendar_staging_table,
    upstream_tasks=[drop_calendar_staging_table])

flow.set_dependencies(
    task=load_calendar_data_into_staging_table,
    upstream_tasks=[create_calendar_staging_table])

# COVID JAPAN DATA.
flow.set_dependencies(
    task=drop_covid_staging_table)

flow.set_dependencies(
    task=create_covid_staging_table,
    upstream_tasks=[drop_covid_staging_table])

flow.set_dependencies(
    task=load_covid_data_into_staging_table,
    upstream_tasks=[create_covid_staging_table])

# 2) RUN STAGING TABLES QUALITY CHECKS.
flow.set_dependencies(
    task=run_quality_checks_for_staging_tables,
    upstream_tasks=[load_calendar_data_into_staging_table,
                    load_covid_data_into_staging_table])

# 3) CREATE NEW TABLES FOR SOURCE-OF-TRUTH DB.
flow.set_dependencies(
    task=create_table_tokyo_covid_by_prefecture,
    upstream_tasks=[run_quality_checks_for_staging_tables])

flow.set_dependencies(
    task=create_table_tokyo_aggr_listings_availability,
    upstream_tasks=[run_quality_checks_for_staging_tables])

flow.set_dependencies(
    task=create_table_tokyo_listings_availability_and_covid_rates,
    upstream_tasks=[create_table_tokyo_covid_by_prefecture,
                    create_table_tokyo_aggr_listings_availability])

