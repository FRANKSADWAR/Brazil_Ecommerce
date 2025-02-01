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


CREATE TABLE olist_order_items (
    order_id VARCHAR(255) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    shipping_limit_date TIMESTAMP,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2)
    )


CREATE TABLE olist_order_reviews(
    review_id VARCHAR(255) NOT NULL PRIMARY KEY,
    order_id VARCHAR(255),
    review_score INT,
    review_comment_title VARCHAR(255),
    review_comment_message VARCHAR(255),
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
)

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



-- General sales order count trends
SELECT
  DATE(order_purchase_timestamp) AS date_,
  COUNT(order_id) AS orders
FROM
  olist_orders
WHERE {{ date }}
GROUP BY
  DATE(order_purchase_timestamp)


--- Order purchase date by MONTH, YEAR, WEEK, QUARTER
WITH
  order_dates AS (
    SELECT
      order_id,
      YEAR(order_purchase_timestamp) AS order_year,
      MONTH(order_purchase_timestamp) AS month_no,
      WEEK(order_purchase_timestamp, 1) AS week_no,
      QUARTER(order_purchase_timestamp) AS quarter_no
    FROM
      olist_orders
  )
SELECT CONCAT(order_year, ' Q', quarter_no) AS year_quarter FROM order_dates

--- Order numbers by Quarter
SELECT
  QUARTER(order_purchase_timestamp) AS QUARTER,
  MONTH(order_purchase_timestamp) AS month_no,
  MONTHNAME(order_purchase_timestamp) AS month_nm,
  COUNT(order_id) AS orders
FROM
  olist_orders
WHERE
  YEAR(order_purchase_timestamp) = 2018
GROUP BY
  QUARTER(order_purchase_timestamp),
  MONTHNAME(order_purchase_timestamp)
ORDER BY
  month_no ASC;


-- Count of orders and the difference of orders per quarter
SELECT
  QUARTER(order_purchase_timestamp) AS QUARTER,
  MONTH(order_purchase_timestamp) AS month_no,
  MONTHNAME(order_purchase_timestamp) AS month_nm,
  COUNT(order_id) AS orders,
  MAX(COUNT(order_id)) OVER() AS max_overall_orders,
  MAX(COUNT(order_id)) OVER (PARTITION BY QUARTER(order_purchase_timestamp)) AS max_orders_per_quarter
FROM
  olist_orders
WHERE
  YEAR(order_purchase_timestamp) = 2018
GROUP BY
  QUARTER(order_purchase_timestamp),
  MONTHNAME(order_purchase_timestamp)
ORDER BY
  month_no ASC;



WITH sales_orders_delivered AS (SELECT
  SELECT COUNT(sales.order_id) AS orders_del
  FROM olist_orders AS orders
  WHERE orders.order_status = 'delivered'
)
SELECT * FROM sales_orders_delivered



-- Count of orders per quarter of each year
WITH
  order_dates AS (
    SELECT
      order_id,
      YEAR(order_purchase_timestamp) AS order_year,
      MONTH(order_purchase_timestamp) AS month_no,
      MONTHNAME(order_purchase_timestamp) AS month_name,
      WEEK(order_purchase_timestamp, 1) AS week_no,
      QUARTER(order_purchase_timestamp) AS quarter_no
    FROM
      olist_orders
  )
SELECT 
    COUNT(order_id) AS orders,
    quarter_year
FROM ( 
    SELECT order_id,
    CONCAT('Q',quarter_no,'  ',order_year) AS quarter_year,
    order_year,
    quarter_no
    FROM order_dates 
    ) AS orders
    GROUP BY quarter_year
    ORDER BY order_year ASC, quarter_no ASC

-- Orders by time of day
WITH
  order_dates AS (
    SELECT
      order_id,
      YEAR(order_purchase_timestamp) AS order_year,
      MONTH(order_purchase_timestamp) AS month_no,
      MONTHNAME(order_purchase_timestamp) AS month_name,
      WEEK(order_purchase_timestamp, 1) AS week_no,
      QUARTER(order_purchase_timestamp) AS quarter_no,
      DAYNAME(order_purchase_timestamp) AS day_name,
      DAYOFWEEK(order_purchase_timestamp) AS day_of_week,
      HOUR(order_purchase_timestamp) AS time_of_day
    FROM
      olist_orders
  )
SELECT COUNT(order_id) AS orders, time_of_day FROM order_dates GROUP BY time_of_day
ORDER BY time_of_day ASC


-- Orders by the day of the week
WITH
  order_dates AS (
    SELECT
      order_id,
      YEAR(order_purchase_timestamp) AS order_year,
      MONTH(order_purchase_timestamp) AS month_no,
      MONTHNAME(order_purchase_timestamp) AS month_name,
      WEEK(order_purchase_timestamp, 1) AS week_no,
      QUARTER(order_purchase_timestamp) AS quarter_no,
      DAYNAME(order_purchase_timestamp) AS day_name,
      DAYOFWEEK(order_purchase_timestamp) AS day_of_week
    FROM
      olist_orders
  )
SELECT COUNT(order_id) AS orders, day_name, day_of_week FROM order_dates GROUP BY day_name
ORDER BY day_of_week ASC


-- Count of orders by state
WITH
  orders_region AS (
    SELECT
      orders.order_id,
      orders.customer_id,
      orders.order_status,
      geo.geolocation_city,
      geo.geolocation_state
    FROM
      olist_orders AS orders
      INNER JOIN olist_customers AS customers ON orders.customer_id = customers.customer_id
      INNER JOIN olist_geolocation AS geo ON customers.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
  )
SELECT
  COUNT(DISTINCT order_id) AS orders,
  geolocation_state AS state
FROM
  orders_region
GROUP BY
  geolocation_state
ORDER BY orders DESC


-- Cluster map of the sales orders placed through the platform
WITH
  orders_region AS (
    SELECT
      orders.order_id,
      orders.customer_id,
      orders.order_status,
      geo.geolocation_city,
      geo.geolocation_state,
      geo.geolocation_lat AS lat,
      geo.geolocation_lng AS lng
    FROM
      olist_orders AS orders
      INNER JOIN olist_customers AS customers ON orders.customer_id = customers.customer_id
      INNER JOIN olist_geolocation AS geo ON customers.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
  )
SELECT
  COUNT(DISTINCT order_id) AS orders,
  geolocation_city AS city,
  lat,
  lng
FROM
  orders_region
GROUP BY
  geolocation_city
ORDER BY orders DESC


--- Payments through the e-commerce platform
SELECT
  payment_type,
  SUM(payment_value) AS payments
FROM
  olist_order_payments
GROUP BY
  payment_type;


-- Investigate the time it takes to deliver to a customer (Start building the feature dataset)
SELECT
  order_id,
  order_status,
  order_delivered_carrier_date,
  order_purchase_timestamp,
  DATEDIFF(order_delivered_carrier_date, order_purchase_timestamp) AS time_to_deliver_to_carrier,
  DATEDIFF(order_delivered_customer_date, order_purchase_timestamp) AS time_to_deliver_to_customer,
  DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp) AS estimated_delivery_period,
  TIMESTAMP(order_delivered_customer_date) AS order_delivered_customer_date,
  order_estimated_delivery_date
FROM
  olist_orders
WHERE
  order_status = 'delivered';



-- Total sales revenue
SELECT 
  SUM(payment_value) AS total_revenue 
FROM olist_order_payments;

-- Order count vs sales order generated from the platform
WITH
  orders_revenue AS (
    SELECT
      orders.order_id,
      DATE(orders.order_purchase_timestamp) AS order_date,
      MONTH(orders.order_purchase_timestamp) AS month_no,
      YEAR(orders.order_purchase_timestamp) AS yearno,
      pay.payment_value
    FROM
      olist_orders AS orders
      INNER JOIN olist_order_payments AS pay ON orders.order_id = pay.order_id
  )
SELECT
  yearno,
  month_no,
  CONCAT(yearno, ' ', month_no) AS yearmon,
  COUNT(DISTINCT order_id) AS order_count,
  SUM(payment_value) AS revenues,
  (SUM(payment_value)/COUNT(DISTINCT order_count)) AS average_order_value
FROM
  orders_revenue
GROUP BY
  yearno,
  month_no


-- General trend in Sales revenue
WITH
  revenue AS (
    SELECT
      pay.order_id,
      olist_orders.order_purchase_timestamp,
      pay.payment_value
    FROM
      olist_order_payments AS pay
      INNER JOIN olist_orders ON pay.order_id = olist_orders.order_id
    WHERE {{ date }}
  )
SELECT
  DATE(order_purchase_timestamp) AS date_of,
  SUM(payment_value) AS sales_value
FROM
  revenue
GROUP BY
  DATE(order_purchase_timestamp)

-- YEARLY SALES REVENUE TRENDS
WITH
  revenue AS (
    SELECT
      pay.order_id,
      YEAR(olist_orders.order_purchase_timestamp) AS year_no,
      pay.payment_value
    FROM
      olist_order_payments AS pay
      INNER JOIN olist_orders ON pay.order_id = olist_orders.order_id
  )
SELECT
  year_no,
  SUM(payment_value) AS sales_value
FROM
  revenue
GROUP BY
  year_no



-- Monthly sales revenue trends
WITH
  revenue AS (
    SELECT
      SUM(pay.payment_value) AS sales_revenue,
      YEAR(olist_orders.order_purchase_timestamp) AS year_no,
      MONTH(olist_orders.order_purchase_timestamp) AS month_no
    FROM
      olist_order_payments AS pay
      INNER JOIN olist_orders ON pay.order_id = olist_orders.order_id
    GROUP BY
      year_no,
      month_no
  )
SELECT
  sales_revenue,
  CONCAT(year_no, ' ', month_no) AS YEARMON
FROM
  revenue


--- Product category purchases over the years
WITH
  product_category_purchases AS (
    SELECT
      itm.order_id,
      itm.product_id,
      itm.price,
      itm.freight_value,
      DATE(orders.order_purchase_timestamp) AS order_date,
      YEAR(orders.order_purchase_timestamp) AS yearno,
      MONTH(orders.order_purchase_timestamp) AS month_no,
      QUARTER(orders.order_purchase_timestamp) AS quarterno,
      op.product_category
    FROM
      olist_order_items AS itm
      INNER JOIN olist_products AS op ON itm.product_id = op.product_id
      INNER JOIN olist_orders AS orders ON itm.order_id = orders.order_id
    WHERE
       {{ product_category }}
      AND op.product_category IS NOT NULL
  )
SELECT
  yearno,
  month_no,
  CONCAT(yearno, ' ', month_no) AS yearmon,
  product_category,
  SUM(price) AS revenue
FROM
  product_category_purchases
GROUP BY
  yearno,
  month_no,
  product_category
ORDER BY
  yearno ASC,
  month_no ASC


-- Configure the same query for quarters only
WITH
  product_category_purchases AS (
    SELECT
      itm.order_id,
      itm.product_id,
      itm.price,
      itm.freight_value,
      DATE(orders.order_purchase_timestamp) AS order_date,
      YEAR(orders.order_purchase_timestamp) AS yearno,
      MONTH(orders.order_purchase_timestamp) AS month_no,
      QUARTER(orders.order_purchase_timestamp) AS quarterno,
      op.product_category
    FROM
      olist_order_items AS itm
      INNER JOIN olist_products AS op ON itm.product_id = op.product_id
      INNER JOIN olist_orders AS orders ON itm.order_id = orders.order_id
    WHERE
      {{ product_category }}
      AND op.product_category IS NOT NULL
  )
SELECT
  yearno,
  quarterno,
  CONCAT(yearno, ' ', quarterno) AS yearqt,
  product_category,
  SUM(price) AS revenue
FROM
  product_category_purchases
GROUP BY
  yearno,
  quarterno,
  product_category

ORDER BY
  yearno ASC,
  quarterno ASC

--- Sales revenue by product category

WITH
  product_category_purchases AS (
    SELECT
      itm.order_id,
      itm.product_id,
      itm.price,
      itm.freight_value,
      DATE(olist_orders.order_purchase_timestamp) AS order_date,
      YEAR(olist_orders.order_purchase_timestamp) AS yearno,
      MONTH(olist_orders.order_purchase_timestamp) AS month_no,
      QUARTER(olist_orders.order_purchase_timestamp) AS quarterno,
      IFNULL(olist_products.product_category, "Unknown") AS product_category
    FROM
      olist_order_items AS itm
      INNER JOIN olist_products ON itm.product_id = olist_products.product_id
      INNER JOIN olist_orders ON itm.order_id = olist_orders.order_id
  )
SELECT
  "Products" AS all_products,
  product_category,
  SUM(price) AS revenue_per_product_category
FROM
  product_category_purchases
GROUP BY
  product_category
