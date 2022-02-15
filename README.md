# Udacity Data Engineering Nanodegree - Capstone Project

# Index
- [Project Write Up](#project-write-up)
   - [Scenario/Use Case](#scenariouse-case)
   - [Goal](#goal)
   - [Datasets](#datasets)
   - [Data Model](#data-model)
   - [Technology Stack](#technology-stack)
   - [ETL Pipeline](#etl-pipeline)  
      - [Steps](#steps)  
      - [Frequency](#frequency)  
      - [Graph](#graph)
   - [Different scenarios (thought experiment given by assignment)](#different-scenarios-thought-experiment-given-by-assignment)
- [Project Setup](#project-setup)
- [How to run the app](#how-to-run-the-app)

# Project Write Up
## Scenario/Use Case
Business Analysts at Airbnb want to understand the impact COVID-19 had on bookings and listings 
during the timespan of 2020-2021 in Tokyo, Japan. They need a source-of-truth database with the relevant data.

## Goal
Provide analysts with a **source-of-truth database** for them to be able to run their analysis and get new insights.
Topics of interest could include:
- Active vs inactive listings trends.
- Is there a negative correlation between positive COVID-19 cases and bookings or active listings?
- etc.

## Datasets
- [Tokyo Airbnb Open Data: Tokyo Airbnb as of 28 October 2021](https://www.kaggle.com/tsarromanov/tokyo-airbnb-open-data)
   - `calendar.csv`: Listings' calendar information.
      - Dataset has more than 3 million rows.
      - Columns to use: `listing_id` (integer), `date` (timestamp), `available` (boolean).
      - Filter `date` for timeframe 2021-10-28 to 2021-12-31. 
- [COVID-19 dataset in Japan - Number of Novel Corona Virus 2019 cases in Japan](https://www.kaggle.com/lisphilar/covid19-dataset-in-japan)
   - `covid_jpn_prefecture.csv`: Covid info by prefecture.
      - Dataset has more than 32k rows.
      - Columns to use: `Date` (timestamp), `Prefecture` (string), `Positive` (integer), `Tested` (integer).
      - Filter `Prefecture` for `Tokyo`.
      - Filter `Date` for timeframe 2021-10-28 to 2021-12-31.

*Note:* Ideally the source-of-truth database should contain records for a longer time period than just 2 months, but the kaggle `Tokyo Airbnb` dataset only has a limited amount of data. For the purpose of this exercise I'll continue with this dataset.

## Data Model

### Table `dim_tokyo_aggregated_listings_availability`
- Contains count of total listings (both available and unavailable listings) and 
  count of only available listings by dates for listings in Tokyo.
- Timeframe: 2021-10-28 - 2021-12-31.
- Columns: `date` (timestamp, primary key), `listings_total_count` (integer), `listings_available_count` (integer)
   - `listings_total_count` is the `COUNT()` of all existing listings for a specific date.
   - `listings_available_count` is the `COUNT()` of all listings `where available == True` for a specific date.
- Source dataset: 'Tokyo Airbnb Open Data: Tokyo Airbnb as of 28 October 2021'.

### Table `dim_tokyo_covid_by_prefecture`
- Contains covid data for Tokyo prefecture.
- Timeframe: 2021-10-28 - 2021-12-31.  
- Columns: `date` (timestamp, primary key), `tested_total` (integer), `tested_positive` (integer)
   - Records are filtered by `Prefecture == Tokyo` prior to insertion.
- Source dataset: 'COVID-19 dataset in Japan - Number of Novel Corona Virus 2019 cases in Japan'.

### Table `fact_tokyo_listings_availability_and_covid_rates`
- Contains tokyo listings availability rate and covid rate by date.
- Columns: `date` (timestamp, primary key), `listings_availability_ratio` (float), `positive_covid_cases_ratio` (float),
  `prev_day_percentage_change_listings_availability` (float), `prev_day_percentage_change_positive_covid_cases` (float).
   - `listings_availability_ratio` shows the ratio of `listings_available_count`/ `listings_total_count` for a specific date.
   - `positive_covid_cases_ratio` shows the ratio of `tested_positive`/ `tested_total` for a specific date.
   - `prev_day_percentage_change_listings_availability` shows the percentage increase compared to the previous day for a specific date.
   - `prev_day_percentage_change_positive_covid_cases` shows the percentage increase compared to the previous day for a specific date.
- Source dataset: table `dim_tokyo_aggregated_listings_availability` and table `dim_tokyo_covid_by_prefecture`.

  
## Technology Stack
- Dataflow Automation Tool: [Prefect](https://www.prefect.io/).
   - In this course the only dataflow automation tool we've worked with is Apache Airflow. While that's probably the most commonly used one, it's not the only tool of that type. [Prefect](https://www.prefect.io/) provides all the functionality Airflow provides while offering a slimmed down version that runs just as any other Python file without requiring neither a dedicated server nor a UI. The ease-of-setup and ease-of-use is what makes me prefer Prefect to Airflow for this project.
- DB: Amazon Redshift.
   - This where the source-of-truth database and staging tables live. 
- File Storage: S3.
   - The base dataset (`calendar.csv` and `covid_jpn_prefecture.csv`) lives an S3 bucket. This way, we can more easily upload the data
into the staging tables in the redshift cluster. (AWS cloud technology is optimized to work seamlessly with each other.) 

## ETL Pipeline
### Steps
1. Load datasets into staging tables:
   - The airbnb listings calendar data living on S3 is loaded into the staging table `tokyo_airbnb_calendar`.
   - The covid japan data living on S3 is loaded into the staging table `covid_japan_by_prefecture`. 
2. Run quality checks on staging tables:
   - Compare number of rows in csv file with number rows in staging table.
   - Identify and remove duplicate rows in staging table.
3. Create source-of-truth tables:
   - Use table `tokyo_airbnb_calendar` to create the data for `dim_tokyo_aggregated_listings_availability` table with columns as described in the Data Model.
   - Use table `covid_japan_by_prefecture` to create the data for `dim_tokyo_covid_by_prefecture` table with columns as described in the Data Model.
   - Use table `dim_tokyo_aggregated_listings_availability` and table `dim_tokyo_covid_by_prefecture` to create table `fact_tokyo_listings_availability_and_covid_rate` with columns as described in the Data Model.

### Frequency
How often the ETL pipeline should be run depends on the analyst's need for up-to-date data and the
update frequency of the source datasets. If the source datasets are updated daily, and the analysts
require the most up-to-date data, scheduling the ETL pipeline to run once a day could be sufficient to meet their needs.

### Graph
![ETL Pipeline Graph](./graph.jpg?raw=true "graph")
- A node represents a task, the name inside the node represents the task name. 
- Task names match the function names in the codebase.

## Different scenarios (thought experiment given by assignment)
How would I approach the problem differently under the following scenarios?:
1. If the data was increased by 100x.
2. If the pipelines were run on a daily basis by 7am.
3. If the database needed to be accessed by 100+ people.

Possible approaches:
1. If the data was increasde by 100x, I'd probably want to provide myself with a Spark cluster and move any tasks that rely on in-memory calculations (e.g. staging table quality checks) to be executed on that.
2. If the pipeline needs to on a daily basis by 7am, I'd set up a schedule for it. (Schedules are a basic feature for most data flow automation tools.)
3. If the database needed to be accessed by 100+ people, I'd probably keep the database in Redshift since it's a reliable analytics database. If the data contained sensitive data (e.g. Personal Identifiable Information) I might want to consider adding user roles to make sure that only authorized users can access it.

# Project Setup

## Option A: Docker Setup *(recommended)*
Make sure you have [Docker](https://www.docker.com/) installed.
Run the following command in a terminal to build and run a new container:
```
bash scripts/run_app_in_docker.sh
```
*Note: I recommend this setup to ensure that none of your current local dependencies
gets changed/updated inadvertently.*

## Option B: Local dependencies setup
Make sure you have [Pipenv](https://pipenv.pypa.io/en/latest/) and Python 3.9 installed.
Run the following command in a terminal to install all Python dependencies locally:
```
pipenv install
```

## Add your credentials
Make a copy of the file `dwh.cfg.sample` and call it just `dwh.cfg`. Replace the empty/indicated values with your credentials, 
and leave the filled out values as they are. Make sure not to use any quotation marks.

# How to run the app
Pick one of the setup options outlined above first.

## Create redshift cluster
Create an aws redshift cluster and its necessary aws resources by running:
```
bash scripts/create_aws_redshift_cluster.sh
```

Running that will also populate the file `aws_role_arn.json`.
   
## Run ETL pipeline
Run the ETL pipeline to create the source-of-truth Airbnb Tokyo Covid database by running:
```
bash scripts/run_etl_pipeline.sh
```

### Create the ETL pipeline graph
Automatically generated by [Prefect](https://www.prefect.io/).
Generate a new graph by updating the pipeline, then running the pipeline following 
the instructions provided above, and then copying the file from the
docker container into the host machine by running:
```
docker cp (your container id):/udacity_capstone_project_local/graph.jpg graph.jpg
```

## Delete redshift cluster
Delete the aws redshift cluster and its necessary aws resources by running:
```
bash scripts/delete_aws_redshift_cluster.sh
```
