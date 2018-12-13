import os
import codecs
import pandas as pd

path = os.getcwd()
file = pd.read_csv(path + '\编码匹配.csv', encoding='utf-8')
file_clean = file.drop_duplicates()
file_clean.to_csv(path + '\clean_编码匹配.csv', index= None)