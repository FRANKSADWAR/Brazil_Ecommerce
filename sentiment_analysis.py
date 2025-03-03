import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict
import nltk

import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, RSLPStemmer, SnowballStemmer
nltk.download('stopwords')
nltk.download('rslp')
from viz_utils import donut_plot


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

def replace_breakline(text_list : List):
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
    """
    Replaces occurrences of Brazilian currency patterns in a list of strings with the word 'dinheiro'.

    Args:
        text_list (List): A list of strings, each potentially containing Brazilian currency.

    Returns:
        List: A list of strings with currency patterns replaced by 'dinheiro'.
    """
    if not text_list:
        return []
    pattern = re.compile(r'[R]{0,1}\$[ ]{0,}\d+(,|\.)\d+')
    return [re.sub(pattern, ' dinheiro ',r) for r in text_list]


def re_numbers(text_list):
    """
    Replaces all numeric characters in each string of the input list with the word 'numero'.

    Args:
        text_list (List[str]): A list of strings to process.

    Returns:
        List[str]: A list of strings with numeric characters replaced by 'numero'.
    """
    pattern = re.compile(r'[0-9]')
    return [re.sub(pattern, ' numero ', r) for r in text_list]


def re_negation(text_list):
    """
    Replace negation patterns in a list of text strings with the word 'negação'.

    This function searches for specific negation patterns in each string of the
    provided list and replaces them with the word 'negação'. The patterns include
    various forms of the word 'não' and similar negations.

    Args:
        text_list (List[str]): A list of text strings to process.

    Returns:
        List[str]: A list of text strings with negation patterns replaced.
    """
    pattern = re.compile(r'([nN][ãÃaA][oO]|[ñÑ]| [nN] )')
    return [re.sub(pattern, ' negação ', r) for r in text_list]

def re_special_characters(text_list):
    """
    Remove special characters from each string in a list.

    This function takes a list of strings and removes all non-word characters
    from each string, replacing them with a space.

    Args:
        text_list (List[str]): A list of strings to process.

    Returns:
        List[str]: A list of strings with special characters replaced by spaces.
    """
    pattern = re.compile(r'\W')
    return [re.sub(pattern, ' ', r) for r in text_list]

def re_whitespaces(text_list):
    """
    Remove extra whitespaces from each string in a list.

    This function processes a list of strings, replacing multiple consecutive
    whitespace characters with a single space and removing trailing spaces
    and tabs from each string.

    Parameters:
        text_list (List[str]): A list of strings to be processed.

    Returns:
        List[str]: A list of strings with extra whitespaces removed.
    """
    white_spaces = [re.sub('\s+',' ',r) for r in text_list]
    white_space_removed = [re.sub('[ \t]+$',' ',r) for r in white_spaces]
    return white_space_removed


def stopwords_removal(text, cached_stopwords = stopwords.words('portuguese')):
    """
    Remove Portuguese stopwords from the given text.

    This function takes a string of text and removes all words that are present
    in the list of cached Portuguese stopwords. The comparison is case-insensitive.

    Parameters:
        text (str): The input text from which stopwords are to be removed.
        cached_stopwords (list, optional): A list of stopwords to be removed. 
            Defaults to the Portuguese stopwords from the NLTK library.

    Returns:
        list: A list of words from the input text with stopwords removed.
    """
    return [c.lower() for c in text.split() if c.lower() not in cached_stopwords]


def stemming_process(text, stemmer = RSLPStemmer()):
    """
    Apply stemming to the input text using the specified stemmer.

    Parameters:
        text (str): The input text to be stemmed.
        stemmer (nltk.stem.api.StemmerI, optional): The stemmer to use for stemming. 
            Defaults to RSLPStemmer.

    Returns:
        list: A list of stemmed words from the input text.
    """
    return [stemmer.stem(c) for c in text.split()]


#### Feature Extraction : CountVectorizer, TF-IDF
def extract_features_from_corpus(corpus, vectorizer, df =False):
    """
    Extracts features from a given text corpus using a specified vectorizer.

    Parameters:
        corpus (List[str]): The text corpus from which to extract features.
        vectorizer (BaseEstimator): The vectorizer to use for feature extraction, such as TfidfVectorizer or CountVectorizer.
        df (bool, optional): If True, returns a DataFrame of the features. Defaults to False.

    Returns:
        Tuple[np.ndarray, Optional[pd.DataFrame]]: A tuple containing the feature matrix as a NumPy array and, if requested, a DataFrame with feature names as columns.
    """
    corpus_features = vectorizer.fit_transform(corpus).toarray()
    feature_names = vectorizer.get_feature_names()
    df_corpus_features = None
    if df:
        df_corpus_features = pd.DataFrame(corpus_features, columns=feature_names)
    else:
        df_corpus_features
    return corpus_features, df_corpus_features

def ngrams_count(corpus, ngram_range, n = -1, cached_stopwords = stopwords.words('portuguese')):
    """
    """
    vectorizer = CountVectorizer(stop_words=cached_stopwords, ngram_range= ngram_range).fit(corpus)
    bag_of_words = vectorizer.transform(corpus)
    sum_of_words = bag_of_words.sum(axis = 0)
    words_freq = [(word, sum_of_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x : x[1], reverse= True)
    total_list = words_freq[:n]

    count_df = pd.DataFrame(total_list, columns = ['ngram','count'])
    return count_df



if __name__ == "__main__":
    path = "data/"
    olist_order_reviews = pd.read_csv(path+'olist_order_reviews_dataset.csv')

    df_reviews = olist_order_reviews.loc[:,['review_score','review_comment_message']]
    df_comments = df_reviews.dropna(subset=['review_comment_message'])
    df_comments = df_comments.reset_index(drop = True)
    df_comments.columns = ['score','comment']

    reviews = list(df_comments['comment'].values)
    reviews_breakline = replace_breakline(reviews)
    reviews_hyperlinks = replace_hyperlinks(reviews_breakline)
    df_comments['re_hyperlinks'] = reviews_hyperlinks

    reviews_dates = re_dates(reviews_hyperlinks)
    df_comments['re_dates'] = reviews_dates

    reviews_money = re_money(reviews_dates)
    df_comments['re_money'] = reviews_money

    reviews_numbers = re_numbers(reviews_money)
    df_comments['re_numbers'] = reviews_numbers

    reviews_negation = re_negation(reviews_numbers)
    df_comments['re_negation'] = reviews_negation

    reviews_special_characters = re_special_characters(reviews_negation)
    df_comments['re_special_chars'] = reviews_special_characters

    reviews_whitespaces = re_whitespaces(reviews_special_characters)
    df_comments['re_whitespaces'] = reviews_whitespaces

    pt_stopwords = stopwords.words('portuguese')
    print(f'Total number of Portuguese stop words in ntlk.corpus module : {len(pt_stopwords)}')
    print(pt_stopwords[:10])

    reviews_stopwords = [' '.join(stopwords_removal(review)) for review in reviews_whitespaces]
    df_comments['stopwords_removed'] = reviews_stopwords

    reviews_stemmer = [' '.join(stemming_process(review)) for review in reviews_stopwords]
    df_comments['stemming'] = reviews_stemmer

    ### Creating a count vectorizer
    count_vectorizer = CountVectorizer(max_features = 300, min_df =7, max_df = 0.8, stop_words=pt_stopwords)
    count_features, df_count_features = extract_features_from_corpus(reviews_stemmer, count_vectorizer, df = True)
    print(f'Shape of the count vectorizer feature matrix: {count_features.shape} \n')

    ### Creating a TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features = 300, min_df = 7, max_df=0.8, stop_words=pt_stopwords)
    ## extractng features for the corpus
    tfidf_features, df_tfidf_features = extract_features_from_corpus(reviews_stemmer, tfidf_vectorizer, df=True)
    print(f'Shape of the TF-IDF feature matrix : {tfidf_features.shape}')


    ### Labelling data by mapping the scores to either positive or negative comments
    score_map = {
        1 : 'negative',
        2: 'negative',
        3 : 'positive',
        4: 'positive',
        5: 'positive'
    }
    df_comments['sentiment_label'] = df_comments['score'].map(score_map)
    
    ### Plot to verify the labelled data
    fig, ax = plt.subplot(figsize = (10, 12))
    donut_plot(df_comments.query('sentiment_label in ("positive","negative")'),
               'sentiment_label', 
               label_names = df_comments.query('sentiment_label in ("positive","negative")')['sentiment_label'].value_counts().index,
               ax=ax, colors = ['darkslateblue','crimson'])
    

    ## Lets plot the n-grams to get an idea of how the bag of words look like using the grams
    positive_comments = df_comments[df_comments['sentiment_label'] == "positive"]['stemming']
    negative_comments = df_comments.query('sentiment_label == "negative"')['stemming']

    ## Get the top 10 unigrams (one word)
