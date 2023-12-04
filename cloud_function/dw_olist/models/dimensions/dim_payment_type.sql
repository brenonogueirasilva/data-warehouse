
with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
select 
		payment_type
from order_payments 
group by 1
order by 1
'''
)
) 
	select 
			 {{ dbt_utils.generate_surrogate_key([ 'payment_type' ])}} as id_payment_type, 
			payment_type 
	from 
	external 
