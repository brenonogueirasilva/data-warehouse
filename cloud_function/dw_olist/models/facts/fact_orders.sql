{{ config(materialized='incremental') }}

with external as (
select * from EXTERNAL_QUERY (
'us.cloud_mysql2',
'''
with orders_aux as (
select 
		customers.customer_city,      -- key to dim_city [dim_city]  
		orders.order_status,		  -- key to dim_status_order [orders]
		-- orders.order_id, 
		-- orders.customer_id, 
		DATE(orders.order_purchase_timestamp) as order_purchase_date, 
		DATE(orders.order_delivered_carrier_date) as order_delivered_carrier_date, 
		DATE(orders.order_delivered_customer_date) as order_delivered_customer_date,
		DATEDIFF(orders.order_delivered_customer_date, orders.order_delivered_carrier_date) AS real_time_delivery,
		DATEDIFF(orders.order_delivered_customer_date, orders.order_purchase_timestamp) AS time_to_carry,
		DATEDIFF(orders.order_estimated_delivery_date, orders.order_delivered_carrier_date) AS estimate_time_delivery,
		review_aux.review_answer_date,	
		review_aux.review_score,
		review_aux.count_reviews
from orders
left join customers on (orders.customer_id = customers.customer_id)
left join  (
select  
		order_id,
		MAX(DATE(review_answer_timestamp)) as  review_answer_date,
		SUM(review_score) as review_score,
		count(*) as count_reviews
from orders_reviews
group by 1 
) review_aux on (review_aux.order_id = orders.order_id)
)
select 	
		customer_city,        
		order_status,	
		order_purchase_date,
		order_delivered_carrier_date,
		order_delivered_customer_date,
		review_answer_date,
		SUM(real_time_delivery) as sum_real_time_delivery, 
		SUM(time_to_carry) as  sum_time_to_carry,
		SUM(estimate_time_delivery) as  sum_estimate_time_delivery,
		SUM(review_score) as sum_review_score,
		SUM(count_reviews) as count_reviews, 
		COUNT(*) as count_orders
from orders_aux	
group by 1,2,3,4,5,6
'''
)
) 
	select 
        {{ dbt_utils.generate_surrogate_key([ 'customer_city'])}} as id_customer_city,  
        {{ dbt_utils.generate_surrogate_key([ 'order_status'])}} as id_order_status,       
		order_purchase_date,
		order_delivered_carrier_date,
		order_delivered_customer_date,
		review_answer_date,
		sum_real_time_delivery, 
		sum_time_to_carry,
		sum_estimate_time_delivery,
		sum_review_score,
		count_reviews, 
		count_orders
	from 
	external 


	{% if is_incremental() %}
    where order_purchase_date > (select max(order_purchase_date) from {{this}})
    {% endif %}