import numpy as np
import pandas as pd
import re
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

"""
Before we start tokenization process, we must clean the data and remove special characters, quotations and punctuation marks from
text.
"""
sentence = """ Thomas Jeferson began building Montivello at the\n age of 26."""
pattern = re.compile(r"([-\s.,;:!?])+")
token = [re.sub(pattern, ' ', r) for r in sentence]
grams_2 = list[ngrams(token,2)]
print(grams_2)

"""
1. Tokenization : i. Regex matching and substitution ii.Stop words removal iii. Stemming/Lemmatization
2. Bag-of words model
3. Classification / Topic Modelling
"""

count = CountVectorizer()
docs = np.array(['The sun is shinnig ', 'The sun is out to bless','The sun is shinning and the weather is sweet'])
bag = count.fit_transform(docs)
