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
# Analysis Processes
