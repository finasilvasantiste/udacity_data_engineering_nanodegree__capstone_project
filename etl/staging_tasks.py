from prefect import task
import prefect

@task
def hello_task():
    # TODO: WIP
    logger = prefect.context.get("logger")
    logger.info("Hello world!")