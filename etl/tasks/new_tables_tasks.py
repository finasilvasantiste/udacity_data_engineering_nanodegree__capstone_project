# @task
# def run_quality_checks_for_staging_tables():
#     """
#     Runs quality checks on existing staging tables.
#     The first check confirms the tables are not empty.
#     :return:
#     """
#     # count rows check
#     calendar_staging_table = 'tokyo_airbnb_calendar'
#     covid_staging_table = 'covid_japan_by_prefecture'
#
#     calender_count = int(execute_sql_query_and_get_result(
#             count_rows.format(calendar_staging_table)
#         )[0][0])
#     covid_count = int(execute_sql_query_and_get_result(
#             count_rows.format(covid_staging_table)
#         )[0][0])
#
#     if calender_count <= 0 or covid_count <= 0:
#         raise Exception("One or more staging tables are empty.")