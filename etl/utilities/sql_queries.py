drop_staging_calendar_table = ("""
DROP TABLE IF EXISTS tokyo_airbnb_calendar;
""")

drop_staging_covid_table = ("""
DROP TABLE IF EXISTS covid_japan_by_prefecture;
""")

create_staging_calendar_table = ("""
CREATE TABLE tokyo_airbnb_calendar (
   listing_id NUMERIC PRIMARY KEY,
   date DATE,
   available BOOLEAN,
   price VARCHAR,
   adjusted_price VARCHAR,
   minimum_nights NUMERIC,
   maximum_nights NUMERIC
);
""")

create_staging_covid_table = ("""
CREATE TABLE covid_japan_by_prefecture (
   date DATE,
   Prefecture VARCHAR,
   Positive NUMERIC,
   Tested NUMERIC,
   Discharged NUMERIC,
   Fatal NUMERIC,
   Hosp_require VARCHAR,
   Hosp_severe VARCHAR
);
""")

copy_calendar_data_staging_table = ("""
COPY tokyo_airbnb_calendar 
FROM '{}' 
credentials 'aws_iam_role={}' 
CSV IGNOREHEADER 1 compupdate off region '{}';
""")

copy_covid_data_staging_table = ("""
COPY covid_japan_by_prefecture 
FROM '{}' 
credentials 'aws_iam_role={}' 
CSV IGNOREHEADER 1 compupdate off region '{}';
""")

count_rows = ("""
SELECT COUNT(*) FROM {};
""")

distinct_count_rows = ("""
SELECT DISTINCT COUNT(*) FROM {};
""")

covid_data_filtered_by_tokyo = ("""
SELECT DISTINCT "date", tested as tested_total, positive as tested_positive
FROM covid_japan_by_prefecture
WHERE prefecture ILIKE '%tokyo%'
AND "date" BETWEEN '2021-10-28' AND '2021-12-31'
ORDER BY "date" ASC;
""")

aggr_tokyo_listings_availability = ("""
SELECT total."date", listings_total_count, listings_available_count
FROM (SELECT "date", COUNT(DISTINCT listing_id) as listings_total_count
FROM tokyo_airbnb_calendar
WHERE "date" BETWEEN '2021-10-28' AND '2021-12-31'
GROUP BY "date" ) total JOIN
(SELECT "date", COUNT(DISTINCT listing_id) as listings_available_count
FROM tokyo_airbnb_calendar
WHERE "date" BETWEEN '2021-10-28' AND '2021-12-31'
AND available is True
GROUP BY "date") available ON total."date"=available."date";
""")

tokyo_listings_availability_and_covid_rate = ("""

""")
