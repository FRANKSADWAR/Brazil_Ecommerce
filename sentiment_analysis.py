import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict

import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, RSLPStemmer, SnowballStemmer

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
    This pattern is designed to match dates in the format DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY or DD.MM.YY, let's break down the patterns
    ([0-2][0-9]|(3)[0-1]): This part matches the day of the month
                            [0-2][0-9]: Matches days from 00 to 29
                            (3)[0-1]: Matches days 30 and 31
                            The | is an OR operator, meaning it will match either the first part (00-29) or the second part (30-31)
    (\/|\.|-) This part matches the separator between the day and the month
                            \/ matches the forward slash '/'
                            \. matches the period '.'
                            - matches the hyphen - 
                            | is an OR operator meaning it will match the foward slach,period or hyphen
    (((0)[0-9]) | ((1)[0-2])) This part matches the month
                            (0)[0-9] Matches months from 00 to 09
                            (1)[0-2] Matches months from 10 to 12
                            The | is an OR operator, meaning it will match either first part 00-09 or the second part 10-12
    \d{2,4}: This part matches the year
                            \d matches any digit/integer (0-9)
                            {2,4} specifies that the year can be 2 to 4 digits long (e.g 23 for 2023 or 2023)
    """
    pattern_dd_mm_yyyy = '([0-2][0-9]|(3)[0-1])(\/|\.|-)(((0)[0-9])|((1)[0-2]))(\/|\.|-)\d{2,4}'
    pattern_yyyy_mm_dd = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'
    pattern_mm_dd_yyyy = r'(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}'
    
    def match_date(date_obj):
        if re.match(pattern_dd_mm_yyyy, date_obj):
            return re.sub(pattern_dd_mm_yyyy, ' data ', date_obj)
        elif re.match(pattern_yyyy_mm_dd,  date_obj):
            return re.sub(pattern_yyyy_mm_dd, ' data ',date_obj)
        elif re.match(pattern_mm_dd_yyyy, date_obj):
            return re.sub(pattern_mm_dd_yyyy, ' data ', date_obj)
        else:
            return date_obj
    return [match_date(text) for text in text_list]


def re_money(text_list):
    pattern = '[R]{0,1}\$[ ]{0,}\d+(,|\.)\d+'
    return [re.sub(pattern, ' dinheiro ',r) for r in text_list]

def re_numbers(text_list):
    pattern = '[0-9]'
    return [re.sub(pattern, ' numero ', r) for r in text_list]


def re_negation(text_list):
    pattern = '([nN][ãÃaA][oO]|[ñÑ]| [nN] )'
    return [re.sub(pattern, ' negação ', r) for r in text_list]

def re_special_characters(text_list):
    pattern = '\W'
    return [re.sub(pattern, ' ', r) for r in text_list]

def re_whitespaces(text_list):
    white_spaces = [re.sub('\s+',' ',r) for r in text_list]
    white_space_removed = [re.sub('[ \t]+$',' ',r) for r in white_spaces]
    return white_space_removed


def stopwords_removal(text, cached_stopwords = stopwords.words('portuguese')):
    return [c.lower() for c in text.split() if c.lower() not in cached_stopwords]


def stemming_process(text, stemmer = RSLPStemmer()):
    return [stemmer.stem(c) for c in text.split()]


#### Feature Extraction : CountVectorizer, TF-IDF
def extract_features_from_corpus(corpus, vectorizer, df =False):
    corpus_features = vectorizer.fit_transform(corpus).toarray()
    


if __name__ == "__main__":
    date_list = [
        "Today date is 31/12/2023",
        "The event is on 2023-01-01",
        "The deadline of the assignment is on 12/31/2025",
        "No dates were provided for the trip"
    ]
    links = ["https://erp.agribora.com","Homer was a great movie"]
    link_res = replace_hyperlinks(links)

    results = re_dates(date_list)
    print(results)
    print(link_res)