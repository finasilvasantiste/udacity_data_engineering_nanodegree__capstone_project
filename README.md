# Udacity Data Engineering Nanodegree - Capstone Project

WIP

## Datasets
- [Tokyo Airbnb Open Data: Tokyo Airbnb as of 28 October 2021](https://www.kaggle.com/tsarromanov/tokyo-airbnb-open-data)
   - `calendar.csv`: Listings' calendar information with columns `listing_id` (integer), `date` (timestamp), `available` (boolean).
      - filter `date` for timeframe 2021-10-28 to 2021-12-31. 
- [COVID-19 dataset in Japan - Number of Novel Corona Virus 2019 cases in Japan](https://www.kaggle.com/lisphilar/covid19-dataset-in-japan)
   - `covid_jpn_prefecture.csv`: Covid info by prefecture with columns `Date` (timestamp), `Prefecture` (string), `Positive` (integer), `Tested` (integer).
      - filter `Prefecture` for `Tokyo`.
      - filter `Date` for timeframe 2021-10-28 to 2021-12-31.

*Note:* Ideally the dataset should contain records for a longer time period than just 2 months, but the kaggle `Tokyo Airbnb` dataset only has a limited amount of data.

## Scenario
Business Analysts at Airbnb want to understand the impact COVID-19 had on bookings and listings 
during the timespan of 2020-2021 in Tokyo, Japan. 

### Questions to answer
1. Trends to find out:
   - Active vs inactive listings
   - Bookings
   - Positive COVID-19 cases
2. Correlate trends to each other:
   - Is there a negative correlation between positive COVID-19 cases and bookings or active listings?
   - Does a listings shortage or oversupply exist? If yes, how does it relate to positive COVID-19 cases?
  
## Technology Stack
- Dataflow Automation Tool: [Prefect](https://www.prefect.io/)
- DB: Amazon Redshift
- File Storage: S3


