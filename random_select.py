import codecs
import os
import random

path = os.getcwd()

file = codecs.open(path + '\编码匹配\shanghai\\nlp\\nlp跑上海全部数据.csv', 'r', encoding='utf-8')
file_out = codecs.open(path + '\抽样数据探查.csv', 'w', encoding='utf-8')
list = file.readlines()

random_list = random.sample(range(0, len(list)), 10)

for item in random_list:
    file_out.write(list[item])

file.close()
file_out.close()

