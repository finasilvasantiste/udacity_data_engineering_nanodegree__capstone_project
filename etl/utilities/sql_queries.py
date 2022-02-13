drop_staging_calendar_table = ("""
DROP TABLE IF EXISTS tokyo_airbnb_calendar;
""")

drop_staging_covid_table = ("""
DROP TABLE IF EXISTS covid_japan_by_prefecture;
""")

create_staging_calendar_table = ("""
CREATE TABLE tokyo_airbnb_calendar (
   listing_id NUMERIC PRIMARY KEY,
   date TIMESTAMP,
   available BOOLEAN,
   price VARCHAR,
   adjusted_price VARCHAR,
   minimum_nights NUMERIC,
   maximum_nights NUMERIC
);
""")

create_staging_covid_table = ("""
CREATE TABLE covid_japan_by_prefecture (
   date TIMESTAMP,
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
