from etl.flow import flow


def run_etl_pipeline():
    """
    Runs the etl pipeline to create
    the source-of-truth Airbnb Tokyo Covid database.
    :return:
    """
    flow.run()
    flow.visualize(filename='graph', format='jpg')


if __name__ == "__main__":
    run_etl_pipeline()
