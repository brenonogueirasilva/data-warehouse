{{ config(materialized='incremental') }}

with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
with aux as (
select  
		order_payments.payment_type,	-- dim_payment_type [order_payments]
		DATE(orders.order_purchase_timestamp) as  order_purchase_date, -- dim_date
		order_payments.payment_installments,
		order_payments.payment_value 
from order_payments
left join orders on (order_payments.order_id = orders .order_id) 
) 
	select 
		payment_type,	-- dim_payment_type [order_payments]
		order_purchase_date, -- dim_date
		SUM(payment_installments) as sum_payment_installments,
		SUM(payment_value) as sum_payment_value, 
		count(*) as count_orders_payments 
from aux 
		group by 1,2
'''
)
) 
	select 
            {{ dbt_utils.generate_surrogate_key([ 'payment_type'])}} as id_payment_type, 
            order_purchase_date,
            sum_payment_installments,
            sum_payment_value,
            count_orders_payments
	from 
	external 

	{% if is_incremental() %}
    where order_purchase_date > (select max(order_purchase_date) from {{this}})
    {% endif %}

    