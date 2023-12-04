
with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
select 
		DATE(min(order_purchase_timestamp)) as data_min
	from orders
'''
)
) 
, calendar as (
SELECT
    DATE_ADD( CAST((select data_min from external) as DATE) , INTERVAL n DAY) AS date
  FROM
    UNNEST(GENERATE_ARRAY(0, DATE_DIFF( CAST( current_date() as DATE) , CAST((select data_min from external) as DATE) , DAY))) AS n
) 

    select 
            date,
            EXTRACT(MONTH FROM date) AS month_number,
            FORMAT_DATE('%B', date) AS month_name,
            EXTRACT(YEAR FROM date) AS year
        from calendar


