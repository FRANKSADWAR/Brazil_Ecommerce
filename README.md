# Brazilian Ecommerce Data Modelling & Data Analytics
An end to end data analytics project exploring Brazilian e-commerce market using the 
Olist Brazilian public dataset.
The project demonstrates how raw transaction data can be explored, cleaned, modelled into a relational database and transformed into business insights using Python (data cleaning & exploration), SQL and Metabase.


<a href="https://analytics.luminererp.com/public/dashboard/3fdb94bd-9be6-4c1b-9dbd-974a913ce136?period=2016-01-02~2019-02-01&product_category=computers&product_category=bed_bath_table&product_category=watches_gifts&product_category=home_appliances&product_category=furniture_bedroom&product_category=office_furniture&product_category=electronics&product_category=furniture_decor&tab=5-revenue">Explore the interactive Metabase dashboard</a>.

Table of Contents
- [Project Overview](#project-overview)
- [What This Project Demonstrates](#what-this-project-demonstrates)
- [Dataset, Tools and Technologies](#datasets-tools-technologies)
- [Data Model](#data-model)
- [Analytics Results](#analytics-results)
- [Live Dashboard](#live-dashboard)

## Project Overview
Olist connects small businesses across Brazil to the country's major marketplaces. The public dataset contains roughly **100,000 orders placed between 2016 and 2018** across multiple marketplaces, and lets each order be viewed from several angles:

- **Orders:** status and delivery timeline
- **Cashflow:** price, payment and freight performance
- **Customers:** location
- **Products:** category and attributes
- **Feedback:** customer reviews

A separate geolocation table maps Brazilian zip codes to latitude & longitude coordinates.

The goal of this project is to show the full analytics lifecycle: understand the data, clean it, model it properly into a relational database, and turn it into a self-service dashboard that answers real business questions.

## What This Project Demonstrates

**Data cleaning & EDA**: Profiling, cleaning and visualising the raw CSVs with Pandas and Matplotlib

**Data modelling**: A normalised relational schema built with SQL DDL (keys, relationships, constraints)

**SQL analytics**: Analytical queries over the modelled data to calculate revenue, order and product metrics.

**BI & dashboarding**: An interactive, filterable Metabase dashboard published publicly.

**End-to-end thinking**: Moving from raw files to decision-ready insights in one reproducible workflow.


## Dataset, Tools and Technologies
**Source:** [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

**Python:** Pandas and Matplotlib for data cleaning, exploration and visualization

**SQL (DDL & DML):** schema design and analytical queries

**Metabase:** open-source, self-service analytics platform hosted in a private clous server, used for building the dashboards
## Project Workflow
### 1. Data Exploration
- Loaded each dataset and inspected structure, data types and row counts
- Checked for missing values, duplicates and inconsistent formats
- Converted timestamp columns to proper datetime dtype
- Standardised and translated product categories to English
- Visualised distributions and trends with Matplotlib to build an understanding of the data before modelling
### 2. Data modelling
Designed a relational schema from the cleaned datasets
- Created the tables with **SQL DDL**, defining primary keys, foreign keys and relationships between orders, customers, items, payments, reviews, products and sellers
- Loaded the cleaned data into the database using mysqlimport

### 3. Data analytics
- SQL queries to answer business questions on revenue, orders, regions and products
- Connected Metabase to the database and built questions and charts on top of the model

## Data Model
The data model below shows how the Olist datasets are related:

![Data Model](Images/Data_Model.png)


## Analytics Results
The dashboard looks at the market place from several perspectives.

Sales revenue against orders placed in the platform
![Sales Revenue](Images/image1.png)

Monthly Sales Revenue trends
![Sales revenue trends](Images/image2.png)

![Quarterly sales trends](Images/image3.png)

Revenue trends
![Revenue trends](Images/image4.png)

Ordering trends

![Order Overview](Images/image5.png)

Orders and regions
![Orders and regions](Images/image6.png)

Products analytics
![Products analytics](Images/image7.png)

## Live dashboard
For the full interactive experience, with filters by period and product category, 
use the [live dashboard](https://analytics.luminererp.com/public/dashboard/3fdb94bd-9be6-4c1b-9dbd-974a913ce136?period=2016-01-02~2019-02-01&product_category=computers&product_category=bed_bath_table&product_category=watches_gifts&product_category=home_appliances&product_category=furniture_bedroom&product_category=office_furniture&product_category=electronics&product_category=furniture_decor&tab=5-revenue).