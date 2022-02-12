import prefect
from prefect import task, Flow
from etl.staging_tasks import hello_task


with Flow("airbnb-tokyo-covid-data") as flow:
    hello_task()

flow.run()
