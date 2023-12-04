

with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
select 
		geolocation_city as city, 
		geolocation_state as state  
from geolocation g
group by 1,2
order by 1,2
'''
)
) 
	select 
			 {{ dbt_utils.generate_surrogate_key([ 'city', 'state' ])}} as id_city, 
			city,
            state
	from 
	external 