import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

path = "data/"
olist_order_reviews = pd.read_csv(path+'olist_order_reviews_dataset.csv')

df_reviews = olist_order_reviews.loc[:,['review_score','review_comment_message']]
df_comments = df_reviews.dropna(subset=['review_comment_message'])
df_comments = df_comments.reset_index(drop = True)
df_comments.columns = ['score','comment']