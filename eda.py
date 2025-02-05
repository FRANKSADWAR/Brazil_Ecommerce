import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go
import json

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

