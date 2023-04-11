# e-commerce-data-wrangling
A project for Pacmann's Data Wrangling Course

# Background
The data is from an e-commerce database (olist.db) which consists of many tables. Analysis used here will focus on state and looking at it from different angles.

# Objectives
To understand the e-commerce performance based on:
1. Sales vs Purchase
2. Sales Change over Time
3. Order Time
4. Handling Time
5. Product Price
6. Review

# Flow
1. This project uses given database, olist.db, which is comprised of many tables. All tables are used here except geolocation
2. It is started with some data cleaning which utilizes a Class called Cleaning with three cleaning functions: impute_outliers, impute_null and drop_dupilcates
3. For outliers, the median value is used. For null, it is mode for categorical data and median for numeric
4. After cleansing is done, next step is converting date values into datetype columns
5. For most of the analysis, this projects relies heavily on two self-made tables namely `order_total` and `order_origin` where the first focuses on every aspects of each orders and the latter is similar but with addition of seller and customer's origin
![image](https://user-images.githubusercontent.com/122712029/231193422-5a031a8c-9828-4f85-b821-9e7fe4ca3c89.png)
![image](https://user-images.githubusercontent.com/122712029/231193501-2a25b1a7-8023-4682-9aa7-e7261ff4282e.png)

# Analysis Preparation: Creating Time-related Columns
1. `order_purchase_hr`
2. `order_purchase_day`
3. `order_purchase_month`
4. `order_purchase_year`
5. `order_purchase_dayofweek`
6. `order_delivery_time`
7. `order_estimation_time_gap`
8. `order_process_time`
9. `order_carrier_time`
10. `review_process_time`

# Analysis: Sales vs Purchase
Utilizing customer and seller's place of origin, this section generates how much sales (goods outflow) and purchase (goods inflow) happen in each states.

# Analysis: Sales Change over Time
Using order's timestamp, this section maps how sales change over time for each states and categories

# Order Time
Using newly made columns `order_delivery_time` and `order_estimation_time_gap`, this section show delivery time (actual delivery from seller to customer) and estimation (seller's estimation when customers execute their orders) for every states

# Handling Time
Based on `order_process_time` and `order_carrier_time`, it generates how sellers from each states manage their order shipping which comprises of two phases, namely processing (delivering orders to carrier) and carrier (process of carrier agents delivering goods to customers)

# Product Price
Based on mean price per products, this section shows variance of every product prices from each states

# Review
Using `review_process_time` and `review_score`, it generates two things, how long does it take for customers from each states file review to each sellers and sellers from which states earn the most favorable review score.
