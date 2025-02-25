import numpy as np
import pandas as pd
import re
from nltk.util import ngrams

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
1. Tokenization : i. Regex ii.Stop words iii. Stemming iii.Lemmatization
"""