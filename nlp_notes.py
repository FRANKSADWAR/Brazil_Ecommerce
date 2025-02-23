import numpy as np
import pandas as pd
import re

"""
Before we start tokenization process, we must clean the data and remove special characters, quotations and punctuation marks from
text.
"""
sentence = """ Thomas Jeferson began building Montivello at the\n age of 26."""
tokens = re.split(r'[-\s.,:!?]+', sentence)
tokens