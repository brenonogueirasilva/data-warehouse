
with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
select 
		order_status
from orders 
group by 1 
order by 1 
'''
)
) 
	select 
			 {{ dbt_utils.generate_surrogate_key([ 'order_status' ])}} as id_city, 
            order_status
	from 
	external 