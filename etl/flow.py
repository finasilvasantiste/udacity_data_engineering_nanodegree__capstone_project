import prefect
from prefect import task, Flow
from etl.staging_tasks import create_calendar_staging_table,\
    load_calendar_data_into_staging_table


with Flow("airbnb-tokyo-covid-data") as flow:
    create_calendar_staging_table()
    # load_calendar_data_into_staging_table()

# flow.run()
