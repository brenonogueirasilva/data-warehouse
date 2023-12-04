{{ config(materialized='ephemeral') }}

with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
select 
		product_category_name 
from products 
group by 1
order by 1
'''
)
) 
	select 
			 {{ dbt_utils.generate_surrogate_key([ 'product_category_name' ])}} as id_product_category_name, 
			product_category_name 
	from 
	external 