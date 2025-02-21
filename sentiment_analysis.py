import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict

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



def find_patterns(re_pattern, text_list):
    p = re.compile(re_pattern)
    position_dict = {}
    i = 0
    for c in text_list:
        match_list = []
        iterator = p.finditer(c)
        for match in iterator:
            match_list.append(match.span())
        control_key = f'Text idx {i}'
        if len(match_list) == 0:
            pass
        else:
            position_dict[control_key] = match_list
        i += 1
    return position_dict

def print_step_result(text_list_before, text_list_after, idx_list):
    i = 1
    for idx in idx_list:
        print(f'---Text {i} ---\n')
        print(f'Before: \n {text_list_before[idx]}\n')
        print(f'After -- \n {text_list_after}\n')
        i += 1

def replace_breakline(text_list):
    """
    text_list: a list of strings where each string may contain newline (\n) or carriage return (\r) characters
        Define a regex pattern to match newline and carriage return characters
        Iterate over each string in the input list
        Replace occurances of the pattern in each string with a space
        Return the modified list of strings

    """
    pattern = '[\n\r]'
    return [re.sub(pattern, ' ',r) for r in text_list]


def replace_hyperlinks(text_list : List[str]) -> List[str]:
    """
    text_list: List of strings where each string may contain hyperlinks
    """
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return [re.sub(pattern, ' link ', r) for r in text_list]

    