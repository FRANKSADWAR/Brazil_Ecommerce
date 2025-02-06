import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go
import json
from viz_utils import *

import requests
from PIL import Image

## Reading the files
path = "data/"
olist_customer = pd.read_csv(path + 'olist_customers_dataset.csv')
olist_geolocation = pd.read_csv(path +'olist_geolocation_dataset.csv')
olist_orders = pd.read_csv(path +'olist_orders_dataset.csv')
olist_order_items = pd.read_csv(path+'olist_order_items_dataset.csv')
olist_order_payments = pd.read_csv(path+'olist_order_payments_dataset.csv')
olist_order_reviews = pd.read_csv(path+'olist_order_reviews_dataset.csv')
olist_products = pd.read_csv(path+'olist_products_dataset.csv')
olist_sellers = pd.read_csv(path+'olist_sellers_dataset.csv')

## An overview of the dataset
datasets = [olist_customer, olist_geolocation, olist_orders, olist_order_items, 
            olist_order_payments, olist_order_reviews, olist_products, olist_sellers]

names = ['olist_customer','olist_geolocation','olist_orders', 'olist_orders','olist_order_items','olist_order_payments',
        'olist_order_reviews','olist_products','olist_seller']

### Create a new dataframe
data_info = pd.DataFrame({})
data_info['dataset'] = names
data_info['n_rows'] = [df.shape[0] for df in datasets]
data_info['n_cols'] = [df.shape[1] for df in datasets ]
data_info['null_count'] = [df.isnull().sum().sum() for df in datasets]
data_info['qty_null_columns'] = [len([col for col, null in df.isnull().sum().items() if null > 0]) for df in datasets]
data_info['null_columns'] = [', '.join([col for col, no_null in df.isnull().sum().items() if no_null > 0]) for df in datasets]

data_info.style.background_gradient()

### Exploratory data analysis
# Total orders in the e-commerce platform
df_orders = olist_orders.merge(olist_customer, how = 'left', on ='customer_id')
fig, ax = plt.subplots(figsize = (14,6))
single_countplot(df_orders, x ='order_status', ax = ax)
plt.show()


## Extract the time data type information from the dataset
timestamp_cols = ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_estimated_delivery_date']
for col in timestamp_cols:
    df_orders[col] = pd.to_datetime(df_orders[col])

## Extract the attributes
df_orders['order_purchase_year'] = df_orders['order_purchase_timestamp'].dt.year
df_orders['order_purchase_month'] = df_orders['order_purchase_timestamp'].dt.month
df_orders['order_purchase_month_name'] = df_orders['order_purchase_timestamp'].dt.month_name
df_orders['order_purchase_quarter'] = df_orders['order_purchase_timestamp'].dt.quarter
df_orders['order_purchase_week_no'] = df_orders['order_purchase_timestamp'].dt.isocalendar().week
df_orders['order_purchase_day'] = df_orders['order_purchase_timestamp'].dt.day_name()
df_orders['order_purchase_hour'] = df_orders['order_purchase_timestamp'].dt.hour
df_orders['order_purchase_tod'] = df_orders['order_purchase_timestamp'].dt.strftime('%H:%M:%S')
df_orders['order_purchase_year_month'] = df_orders['order_purchase_timestamp'].dt.strftime('%Y%m')
df_orders['order_purchase_date'] = df_orders['order_purchase_timestamp'].apply(lambda x: x.strftime('%Y%m%d'))
df_orders['order_purchase_dayofweek'] = df_orders['order_purchase_timestamp'].dt.dayofweek
df_orders['order_purchase_dayofweek_name'] = df_orders['order_purchase_timestamp'].apply(lambda x: x.strftime('%a'))


## Bins the hours
hours_bins = [-0.1, 6, 12, 18, 23]
hours_labels = ['Dawn','Morning','Afternoon','Night']
df_orders['order_purchase_time_day'] = pd.cut(df_orders['order_purchase_hour'], hours_bins, labels = hours_labels) ## review pd.cut code

## Creating a figure and GridSpec to collect the visualizations
fig = plt.figure(constrained_layout = True, figsize=(14,11))

## Define the axes
gs = GridSpec(2,2, figure=fig)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1 ,0])
ax3 = fig.add_subplot(gs[1, 1])

## Add the plots to the sub-plots
sns.lineplot(data = df_orders['order_purchase_year_month'].value_counts().sort_index(),
            ax = ax1, color = 'darkslateblue', linewidth =2)

ax1.annotate(f'Highest Orders \nReceived', (13,7500),
    xytext=(-75, -25), textcoords = 'offset points', bbox = dict(boxstyle = "round4", fc="w", pad = 0.8),
    arrowprops=dict(arrowstyle='-|>', fw='w'), color = 'dimgrey', ha = 'center'
)

ax1.annotate(f'Noise on data \n (huge decrease)', (23,0), xytext = (48,25),
    textcoords='offset points', bbox = dict(boxstyle="round4", fc="w", pad = 0.5),
    arrowprops=dict(arrowstyle='-|>', fc="w"), color = 'dimgrey', ha ='center'
)

format_spines(ax1, right_border= False)

for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
ax1.set_title('Trend of Orders in Brazil E-commerce', size =14, color = 'dimgrey')


## Create a bar chart for total orders by day of week
single_countplot(df_orders, x = 'order_purchase_dayofweek', ax = ax2, order =False, palette='YlGnBu')
weekday_label = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
ax2.set_xticklabels(weekday_label)
ax2.set_title('Total orders by Day of Week', size = 14, color ='dimgrey', pad = 20)

## Create a bar chart

