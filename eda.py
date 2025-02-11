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
df_orders['order_purchase_month_name'] = df_orders['order_purchase_timestamp'].dt.month_name()
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

## Create a bar chart for orders by time of day
day_color_list = ['darkslateblue','deepskyblue','darkorange','purple']
single_countplot(df_orders, x ='order_purchase_time_day', ax = ax3, order = False, palette=day_color_list)
ax3.set_title('Total orders by time of day', size = 14, color = 'dimgrey', pad =20)

plt.tight_layout()
plt.show()


### ---- A comparison between 2017 and 2018
fig = plt.figure(constrained_layout = True)

## Define the axis
gs = GridSpec(1, 3, figure = fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1:])

## Annotation Comparison of Order trends on e-commerce between 2017 and 2018
df_orders_compare = df_orders.query('order_purchase_year in (2017,2018) & order_purchase_month <= 8')
year_orders = df_orders_compare['order_purchase_year'].value_counts()
growth =  int(round(100 *(1 + year_orders[2017] / year_orders[2018]),0))
ax1.text(0.0, 0.73, f'{year_orders[2017]}', fontsize = 40, color ='mediumseagreen', ha='center')
ax1.text(0.00, 0.64, 'orders registered in 2017 \n between January and August', fonsize = 60, color = 'darkseablue', ha='center')
ax1.text(0.00, 0.31, 'orders registered in 2018 \n between January and August', fontsize = 10, ha='center')
signal = '+' if growth > 0 else '-'
ax1.text(0.00, 0.20, f'{signal}{growth}%', fontsize = 14, ha='center',color ='white',
        style='italic', weight ='bold', bbox = dict(facecolor = 'navy', alpha =0.5, pad =10, boxstyle ='round', pad =0.7))
ax1.axis('off')

## Bar chart comparison of sales in 2017 and 2018
single_countplot(df_orders, x ='order_purchase_month', hue ='order_purchase_year', ax = ax2, order = False, palette = 'YlGnBu')
month_label = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']
ax2.set_xticklabels(month_label)
ax2.set_title('Orders comparison between 2017 and 2018 : January to August',size = 12, color= 'dimgrey', pad =20)
plt.legend(loc = 'lower right')
plt.show()


### USing geo-location to analyze the Brazil e-commerce data
df_orders_items = df_orders.merge(olist_order_items, how ='left', on='order_id')
r = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes")
content = [c['UF'] for c in json.loads(r.text)]
br_info = pd.DataFrame(content)
br_info['nome_regiao'] = br_info['regiao'].apply(lambda x: x['nome'])
br_info.drop('regiao', axis =1, inplace =True)
br_info.drop_duplicates(inplace= True)


## clipping locations to those within the Brazilian map
geo_prep = olist_geolocation[olist_geolocation.geolocation_lat <= 5.27438888]
geo_prep = geo_prep[geo_prep.geolocation_lng >= -73.98283055]
geo_prep = geo_prep[geo_prep.geolocation_lat >= -33.75116944]
geo_prep = geo_prep[geo_prep.geolocation_lng <= -34.79314722]

geo_group = geo_prep.groupby(by = 'geolocation_zip_code_prefix', as_index = False).min()

## Merging all information
df_order_items = df_orders_items.merge(br_info, how ='left', left_on ='customer_state', right_on ='sigla')
df_order_items = df_order_items.merge(geo_group, how ='left', 
                    left_on = 'customer_zip_code_prefix',
                    right_on= 'geolocation_zip_code_prefix')

df_orders_items.head()


### A summary of the orders by region, state and city
df_orders_filt = df_order_items[(df_order_items['order_purchase_year_month'].astype(int) >= 201701)]
df_orders_filt = df_orders_filt[(df_orders_filt['order_purchase_year_month'].astype(int) <= 201808)]

# Groupng the data filter by region
df_regions_group = df_orders_filt.groupby(by=['order_purchase_year_month','nemo_regiao'], as_index = False)
df_regions_group = df_regions_group.agg({'customer_id':'count', 'price':'sum'}).sort_values(by='order_purchase_year_month')

df_regions_group.columns = ['month', 'region','order_count','order_amount']
df_regions_group.reset_index(drop = True, inplace= True)

### Group the data by city and get only the top 10 cities
df_cities_group = df_orders_filt.groupby(by="geolocation_city", as_index= False).count().loc[:,['geolocation_city', 'order_id']]
df_cities_group = df_cities_group.sort_values(by='order_id', ascending= False).reset_index(drop = True)
df_cities_group = df_cities_group.iloc[:10, :]

## Creating and preparing figure and axis
fig = plt.figure(constrained_layout = True, figsize =(16,10))
gs = GridSpec(2, 2, figure = fig)
ax1 = fig.add_subplot(gs[0, 0]) ## occupy the first row and first column
ax2 = fig.add_subplot(gs[1, 0]) ## occupy the second row and first column
ax3 = fig.add_subplot(gs[:, 1]) ## occupy the whole row height in the first (1) position

sns.lineplot(x='month', y = 'order_count', ax = ax1, data = df_regions_group, 
            hue ='region',size = 'region', style='region', palette='magma', markers =['o'] * 5)

format_spines(ax1, right_border=False)
ax1.set_title('Evolution of e-commerce in the Brazillian States', size = 12, color = 'dimgrey')
ax1.set_ylabel('Orders')

## Top cities with high order volume
sns.barplot()

















































