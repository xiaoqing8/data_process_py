import os
import codecs
import pandas as pd

path = os.getcwd()
file = pd.read_csv(path + '\第一位编码不同的诊断描述.csv', encoding='utf-8')

