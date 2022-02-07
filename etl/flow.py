import prefect
from prefect import task, Flow


@task
def hello_task():
    # TODO: WIP
    logger = prefect.context.get("logger")
    logger.info("Hello world!")


with Flow("airbnb-tokyo-covid-data") as flow:
    hello_task()

flow.run()
