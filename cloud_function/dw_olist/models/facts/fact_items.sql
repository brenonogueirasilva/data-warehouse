{{ config(materialized='incremental') }}

with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
with aux as (
select 		 
			products.product_category_name, 	-- dim_product_category_name 
			DATE(order_items.shipping_limit_date) as shipping_limit_date,	-- dim_date 
			order_items.price, 
			order_items.freight_value 
from order_items
left join products on (order_items.product_id = products.product_id)
) 
	select 
			product_category_name, 	-- dim_product_category_name 
			shipping_limit_date,	-- dim_date 
			sum(price) as sum_price, 
			sum(freight_value) as sum_freight_value,
			count(*) as count_order_items
	from aux 
	group by 1,2
'''
)
)
    select 
        {{ dbt_utils.generate_surrogate_key([ 'product_category_name'])}} as id_product_category_name, 
        shipping_limit_date,
        sum_price,
        sum_freight_value,
        count_order_items  
    from external


	{% if is_incremental() %}
    where shipping_limit_date > (select max(shipping_limit_date) from {{this}})
    {% endif %}





