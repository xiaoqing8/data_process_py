import os
import codecs
import pandas as pd

path = os.getcwd()

# file = pd.read_csv(path + '\\nlp\第一位编码不同的诊断描述.csv', encoding='utf-8')
# list = file['算法结果'].tolist()
#
# print(len(list))
# count = 0
# for item in list:
#     if item == '0':
#         count += 1
# print(count)

from histogram import graphic
data_name = ('上海表中不确定数据的数据分布')
table_name = (u'完全一样', u'1_不同', u'2_不同', u'3_不同', u'4_不同', u'CDC是父节点', u'CDC是子节点', u'没有找到')  # table_name
title = '上海表中不确定数据的数据分布'
data_value = (0.012, 0.060, 0.021, 0.094, 0.061, 0.38, 0.32, 0.052)
graphic(data_name, table_name, data_value, title, 0.38, os.getcwd()+'\不确定数据的数据分布.png')