import pandas as pd
import os
import emoji 

from classes.secret_manager import SecretManager
from classes.mysql import MySql

file_path = "C:/Users/breno/Downloads/archive/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  './apt-theme-402300-32506a51a70d.json'

project_id = "apt-theme-402300"
secret_id = "mysql-creds"

secret = SecretManager()
mysql_credentials = secret.access_secret_json_file(project_id, secret_id)
mysql_connector = MySql(
    host= mysql_credentials['host'],
    user= mysql_credentials['user'],
    password= mysql_credentials['password'],
    database= 'olist_ecommerce'
)

#Primary Keys
df_products = pd.read_csv(file_path + 'olist_products_dataset.csv')
df_geolocation = pd.read_csv(file_path + 'olist_geolocation_dataset.csv')
df_geolocation.drop_duplicates(subset=['geolocation_zip_code_prefix'], inplace=True)
df_sellers = pd.read_csv(file_path + 'olist_sellers_dataset.csv')
df_sellers = df_sellers[ df_sellers['seller_zip_code_prefix'].isin(df_geolocation['geolocation_zip_code_prefix']) ] 
df_customers = pd.read_csv(file_path + 'olist_customers_dataset.csv')
df_customers = df_customers[ df_customers['customer_zip_code_prefix'].isin(df_geolocation['geolocation_zip_code_prefix']) ] 


#Foreign Key
df_orders = pd.read_csv(file_path + 'olist_orders_dataset.csv')
df_orders = df_orders.astype({
    'order_purchase_timestamp' : 'datetime64[ns]', 
    'order_approved_at' : 'datetime64[ns]',
    'order_delivered_carrier_date' : 'datetime64[ns]',
    'order_delivered_customer_date' : 'datetime64[ns]',
    'order_estimated_delivery_date' : 'datetime64[ns]'
    })
df_orders = df_orders[ df_orders['customer_id'].isin(df_customers['customer_id']) ]
df_order_payments = pd.read_csv(file_path + 'olist_order_payments_dataset.csv')
df_order_payments = df_order_payments[ df_order_payments['order_id'].isin(df_orders['order_id']) ]
df_order_reviews = pd.read_csv(file_path + 'olist_order_reviews_dataset.csv')
df_order_reviews = df_order_reviews.astype({
    'review_creation_date' : 'datetime64[ns]', 
    'review_answer_timestamp' : 'datetime64[ns]',
    'review_comment_title' : 'string', 
    'review_comment_message' : 'string'
    })
df_order_reviews = df_order_reviews[ ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_creation_date', 'review_answer_timestamp'] ] 
df_order_reviews.drop_duplicates(subset=['review_id'], inplace=True)
df_order_reviews.fillna('VAZIO')
df_order_reviews['review_comment_title'] = df_order_reviews['review_comment_title'].apply(lambda s: emoji.replace_emoji(str(s), ''))
df_order_reviews = df_order_reviews[ df_order_reviews['order_id'].isin(df_orders['order_id']) ]
df_order_items = pd.read_csv(file_path + 'olist_order_items_dataset.csv')
df_order_items = df_order_items.astype({
    'shipping_limit_date' : 'datetime64[ns]'
    })
df_order_items = df_order_items[ df_order_items['order_id'].isin(df_orders['order_id']) ]
df_order_items = df_order_items[df_order_items['product_id'].isin(df_products['product_id'])]
df_order_items = df_order_items[ df_order_items['seller_id'].isin(df_sellers['seller_id']) ] 

#Primary Key
sql_create_products = '''
CREATE TABLE IF NOT EXISTS products (
    product_id                      VARCHAR(255) PRIMARY KEY,
    product_category_name           VARCHAR(255),
    product_name_lenght             DECIMAL(10, 2),
    product_description_lenght      FLOAT,
    product_photos_qty              FLOAT,
    product_weight_g                FLOAT,
    product_length_cm               FLOAT,
    product_height_cm               FLOAT,
    product_width_cm                FLOAT
);
'''
sql_create_geolocation = '''
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix     INT PRIMARY KEY,
    geolocation_lat                 FLOAT,
    geolocation_lng                 FLOAT,
    geolocation_city                VARCHAR(255),
    geolocation_state               VARCHAR(255)
);
'''


#Foreign Key
sql_create_sellers = '''
CREATE TABLE IF NOT EXISTS sellers (
    seller_id                       VARCHAR(255) PRIMARY KEY,
    seller_zip_code_prefix          INT,
    seller_city                     VARCHAR(255),
    seller_state                    VARCHAR(255),
    FOREIGN KEY (seller_zip_code_prefix) REFERENCES geolocation(geolocation_zip_code_prefix)
);
'''
sql_create_customers = '''
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(255)        PRIMARY KEY,
    customer_unique_id              VARCHAR(255),
    customer_zip_code_prefix        INT,
    customer_city                   VARCHAR(255),
    customer_state                  VARCHAR(255),
    FOREIGN KEY (customer_zip_code_prefix) REFERENCES geolocation(geolocation_zip_code_prefix)
);
'''
sql_create_orders = '''
CREATE TABLE IF NOT EXISTS orders (
    order_id                        VARCHAR(255) PRIMARY KEY,
    customer_id                     VARCHAR(255),
    order_status                    VARCHAR(255),
    order_purchase_timestamp        TIMESTAMP,
    order_approved_at               TIMESTAMP,
    order_delivered_carrier_date    TIMESTAMP,
    order_delivered_customer_date   TIMESTAMP,
    order_estimated_delivery_date   DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
'''
sql_order_payments = '''
CREATE TABLE IF NOT EXISTS order_payments (
    order_id                        VARCHAR(255),
    payment_sequential              INT,
    payment_type                    VARCHAR(255),
    payment_installments            INT,
    payment_value                   DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
'''
sql_order_reviews = '''
CREATE TABLE IF NOT EXISTS orders_reviews (
    review_id                       VARCHAR(255) PRIMARY KEY,
    order_id                        VARCHAR(255),
    review_score                    INT,
    review_comment_title            VARCHAR(255),           
    review_creation_date            DATE,
    review_answer_timestamp         TIMESTAMP,                  
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
'''
sql_order_items = '''
CREATE TABLE IF NOT EXISTS order_items (
    order_id                        VARCHAR(255),
    order_item_id                   INT,
    product_id                      VARCHAR(255),                   
    seller_id                       VARCHAR(255),                     
    shipping_limit_date             TIMESTAMP,
    price                           DECIMAL(10, 2),
    freight_value                   DECIMAL(10, 2),                     
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
'''

mysql_connector.ddl_operation(sql_create_products)
mysql_connector.ddl_operation(sql_create_geolocation)
mysql_connector.ddl_operation(sql_create_sellers)
mysql_connector.ddl_operation(sql_create_customers)
mysql_connector.ddl_operation(sql_create_orders)
mysql_connector.ddl_operation(sql_order_payments)
mysql_connector.ddl_operation(sql_order_reviews)
mysql_connector.ddl_operation(sql_order_items)

mysql_connector.insert_df(df_products, 'products')
mysql_connector.insert_df(df_geolocation, 'geolocation')
mysql_connector.insert_df(df_sellers, 'sellers')
mysql_connector.insert_df(df_customers, 'customers')
mysql_connector.insert_df(df_orders, 'orders')
mysql_connector.insert_df(df_order_payments, 'order_payments')
mysql_connector.insert_df(df_order_reviews, 'orders_reviews')
mysql_connector.insert_df(df_order_items, 'order_items')