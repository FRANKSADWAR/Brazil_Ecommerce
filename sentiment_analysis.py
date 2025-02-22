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
    Replaces hyperlinks in a list of strings with the word 'link'
    Args:
        text_list (List[str]): List of strings where each string may contain hyperlinks
    Returns:
        List[str] : A list of strings with hyperlinks replaced by the word 'link'
    Lets breakdown the regrex expression:
    http[s]?:// which could be replaced by (?:http|https|ftp|sftp)://
        http: matches the literal text "http"
        [s]? : matches an optional "s" making it work for both https:// and http://
        :// matches literal characters "://" which usually appear in a valid URL
    (?:) is a non-capturing group, meaning it groups elements together without storing them for back-referencing
    [a-zA-Z]|[0-9]|[$-_@#.&+]: [a-zA-Z] matches any letter, lowercase or uppercase
                                [0-9]   matches any digit between 0 to 9
                                [$-_@#.&+] matches common special characters found in URLs

    [!*\(\),] matches more allowed special characters found in URLs
    (?:%[0-9a-fA-F][0-9a-fA-F]): (?:) the non-capturing group
                                 % matches a percentage sign
                                 [0-9a-fA-F] matches a hexadecimal digit
                                 [0-9a-FA-F] matches another hexadecimal digit
    + any or all of the above patterns, the + quantifier at the end ensures that the URL must contain at least one or more of 
            the allowed characters, meaning http:// or https:// alone will not match, there must be additional characters
    """
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return [re.sub(pattern, ' link ', r) for r in text_list]

def re_dates(text_list:List[str]) -> List[str]:
    """
    Args:
        text_list (List[str]) : List of strings where each string may contain date objects
    Returns:
        List[str] : a list object where the date object has been replaced by the word 'data'
    This pattern is designed to match dates in the format DD/MM/YYYY, DD.MM.YYYY or DD.MM.YY, let's break down the patterns
    ([0-2][0-9]|(3)[0-1]): This part matches the day of the month
                            [0-2][0-9]: Matches days from 00 to 29
                            (3)[0-1]: Matches days 30 and 31
                            The | is an OR operator, meaning it will match either the first part (00-29) or the second part (30-31)
    """
    pattern = '([0-2][0-9]|(3)[0-1])(\/|\.)(((0)[0-9])|((1)[0-2]))(\/|\.)\d{2,4}'
    return [re.sub(pattern, ' data ', r) for r in text_list]
    