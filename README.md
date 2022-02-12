# Udacity Data Engineering Nanodegree - Capstone Project

# Index
- [Project Write Up](./README.md#project-write-up)
   - [Scenario/Use Case](./README.md#scenariouse-case)
   - [Datasets](./README.md#datasets)
   - [Data Model](./README.md#data-model)
   - [Technology Stack](./README.md#technology-stack)
   - [ETL Pipeline](./README.md#etl-pipeline)  
- [Project Setup](./README.md#project-setup)
- [How to run the app](./README.md#how-to-run-the-app)

# Project Write Up
## Scenario/Use Case
Business Analysts at Airbnb want to understand the impact COVID-19 had on bookings and listings 
during the timespan of 2020-2021 in Tokyo, Japan. They need a source-of-truth database with the relevant data.

### Questions analysts need to answer
1. Trends to find out:
   - Active vs inactive listings
   - Bookings
   - Positive COVID-19 cases
2. Correlate trends to each other:
   - Is there a negative correlation between positive COVID-19 cases and bookings or active listings?
   - Does a listings shortage or oversupply exist? If yes, how does it relate to positive COVID-19 cases?

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

### Table `dim_aggregated_listings_availability`
- Columns: `date` (timestamp, primary key), `listings_total` (integer), `listings_available` (integer)
   - `listings_total` is the `COUNT()` of all existing listings for a specific date.
   - `listings_available` is the `COUNT()` of all listings `where available == True` for a specific date.
- Source dataset: Tokyo Airbnb Open Data: Tokyo Airbnb as of 28 October 2021.

### Table `dim_tokyo_covid_by_prefecture`
- Columns: `date` (timestamp, primary key), `tested_total` (integer), `tested_positive` (integer)
   - Records are filtered by `Prefecture == Tokyo` prior to insertion.
- Source dataset: COVID-19 dataset in Japan - Number of Novel Corona Virus 2019 cases in Japan.

### Table `fact_tokyo_airbnb_availability_and_covid_rate`
- Columns: `date` (timestamp, primary key), `listings_availability_rate` (float), `positive_covid_cases_rate` (float)
   - `listings_availability_rate` shows the ratio of `listings_available`/ `listings_total` for a specific date.
   - `positive_covid_cases_rate` shows the ratio of `tested_positive`/ `tested_total` for a specific date.
- Source dataset: table `dim_aggregated_listings_availability` and table `dim_tokyo_covid_by_prefecture`.

  
## Technology Stack
- Dataflow Automation Tool: [Prefect](https://www.prefect.io/).
   - In this course the only dataflow automation tool we've worked with is Apache Airflow. While that's probably the most commonly used one, it's not the only tool of that type. [Prefect](https://www.prefect.io/) provides all the functionality Airflow provides while offering a slimmed down version that runs just as any other Python file without requiring neither a dedicated server nor a UI. The ease-of-setup and ease-of-use is what makes me prefer Prefect over Airflow for this project.
- DB: Amazon Redshift.
   - This where the source-of-truth database and staging tables will live. 
- File Storage: S3.
   - The datasets are too big (more than 200mb) to upload to a github repository. To make them accessible for the ETL pipeline I'll use S3 file storage.


## ETL Pipeline
1. Load datasets into staging tables:
   - `calendar.csv` is loaded into the staging table `tokyo_airbnb_calendar`.
   - `covid_jpn_prefecture.csv` is loaded into the staging table `covid_by_japan_prefecture`. 
2. Run quality checks on staging tables:
   - Compare number of rows in csv file with number rows in staging table.
   - Identify and remove duplicate rows in staging table.
3. Create source-of-truth tables:
   - Use table `tokyo_airbnb_calendar` to create the data for `dim_aggregated_listings_availability` table with columns as described in the Data Model.
   - Use table `covid_by_japan_prefecture` to create the data for `dim_tokyo_covid_by_prefecture` table with columns as described in the Data Model.
   - Use table `dim_aggregated_listings_availability` and table `dim_tokyo_covid_by_prefecture` to create table `fact_tokyo_airbnb_availability_and_covid_rate` with columns as described in the Data Model.
   - Quality checks to run before inserting data into db:
      - Identify and remove duplicate rows.
      - Confirm result set is not empty.

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
You can generate a new graph by running:
```
docker cp (your container id):/udacity_capstone_project_local/graph.jpg graph.jpg
```

## Delete redshift cluster
Delete the aws redshift cluster and its necessary aws resources by running:
```
bash scripts/delete_aws_redshift_cluster.sh
```
   
