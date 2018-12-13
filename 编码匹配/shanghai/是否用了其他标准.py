from read_file import ICD_match
import codecs
import os
import pandas as pd

path = os.getcwd()
dic_inte_ICD = ICD_match('系统对照表', 'shanghai')

table = pd.read_csv(path + '\编码匹配.csv', encoding='utf-8')

cause = table['数据集中诊断名称'].tolist()
ICD = table['数据集中诊断编码'].tolist()

for index in range(len(cause)):
    if list(dic_inte_ICD.keys())[list(dic_inte_ICD.values()).index(cause[index].replace('，', ','))] != ICD[index]:
        print(cause[index], ICD[index], list(dic_inte_ICD.keys())[list(dic_inte_ICD.values()).index(cause[index])])