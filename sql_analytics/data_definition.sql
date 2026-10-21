-- CREATE THE RELATIONAL DATA MODEL

CREATE DATABASE brazil_ecommerce;


CREATE TABLE olist_geolocation (
    geolocation_zip_code_prefix BIGINT NOT NULL PRIMARY KEY,
    geolocation_lat DECIMAL(10, 7) NOT NULL,
    geolocation_lng DECIMAL(10, 7) NOT NULL,
    geolocation_city VARCHAR(100) NOT NULL,
    geolocation_state VARCHAR(100) NOT NULL,
    INDEX(geolocation_zip_code_prefix)
)
ALTER TABLE olist_geolocation DROP INDEX idx_geolocation_zip_code;



CREATE TABLE olist_customers (
    customer_id VARCHAR(255) NOT NULL PRIMARY KEY,
    customer_zip_code_prefix BIGINT NOT NULL
)
CREATE INDEX customer_idx ON olist_customers(customer_zip_code);


CREATE TABLE olist_sellers(
    seller_id VARCHAR(255) NOT NULL PRIMARY KEY,
    seller_zip_code_prefix BIGINT NOT NULL,
    FOREIGN KEY(seller_zip_code_prefix) REFERENCES olist_geolocation(geolocation_zip_code_prefix) ON DELETE CASCADE
)
CREATE INDEX idx_olist_sellers ON olist_sellers(seller_id);


CREATE TABLE olist_products(
    product_id VARCHAR(255) NOT NULL PRIMARY KEY,
    product_name_length VARCHAR(255),
    product_description_length DECIMAL(10, 1),
    product_photos_qty DECIMAL(10, 1),
    product_weight_g DECIMAL(10, 1),
    product_length_cm DECIMAL(10, 1),
    product_height_cm DECIMAL(10,1),
    product_width_cm DECIMAL(10,1),
    product_category VARCHAR(255)
)
CREATE INDEX product_category_idx ON olist_products(product_category);


CREATE TABLE olist_orders(
    order_id VARCHAR(255) NOT NULL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    order_status VARCHAR(100),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES olist_customers(customer_id) ON UPDATE CASCADE
)
CREATE INDEX purchase_time_idx ON olist_orders(order_purchase_timestamp);
CREATE INDEX customer_ids ON olist_orders(customer_id);


CREATE TABLE olist_order_items (
    order_id VARCHAR(255) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    shipping_limit_date TIMESTAMP,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2)
)
CREATE INDEX item_id_idx ON olist_order_items(order_item_id);
  


CREATE TABLE olist_order_reviews(
    review_id VARCHAR(255) NOT NULL PRIMARY KEY,
    order_id VARCHAR(255),
    review_score INT,
    review_comment_title VARCHAR(255),
    review_comment_message VARCHAR(255),
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
)
CREATE INDEX order_id_idx ON olist_order_reviews(order_id);

CREATE TABLE olist_order_payments(
    order_id VARCHAR(255) NOT NULL,
    payment_sequential INT,
    payment_type VARCHAR(100),
    payment_installments INT,
    payment_value DECIMAL(10, 2)
)


-- Index the tables to have a better query perfomance
ALTER TABLE olist_orders
ADD INDEX orders_idx (order_id, customer_id);
ALTER TABLE olist_orders
ADD INDEX orders_idx (order_id);

