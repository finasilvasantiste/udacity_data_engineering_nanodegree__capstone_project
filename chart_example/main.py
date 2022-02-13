import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from etl.utilities.db_utility import execute_sql_query_and_get_result_as_df


def create_line_chart():
    query ='''
    SELECT * FROM fact_tokyo_listings_availability_and_covid_rates;
    '''
    data_df = execute_sql_query_and_get_result_as_df(query)
    data_df.plot().get_figure().savefig('line_chart.png')

    # x = [1, 2, 3, 4, 5]
    # y = [3, 3, 3, 3, 3]
    #
    # # plot lines
    # plt.plot(x, y, label="line 1")
    # plt.plot(y, x, label="line 2")
    # plt.plot(x, np.sin(x), label="curve 1")
    # plt.plot(x, np.cos(x), label="curve 2")
    # plt.legend()
    # # plt.show()
    # plt.savefig("line_chart.png")


if __name__ == "__main__":
    create_line_chart()
