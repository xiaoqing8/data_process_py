import pandas as pd
import os
import codecs
from read_file import get_standard_ICD

path = os.getcwd()
file = pd.read_csv(path + '\编码不同.csv', encoding='utf-8')
file = file.drop_duplicates(subset=['诊断名称', '诊断编码', '算法结果'], keep='first')

file_out = codecs.open(path + '\编码不同的数据对照表.csv', 'w', encoding='utf-8')
file_out.write('CDC诊断名称,算法结果,算法结果对应的诊断名称' + '\n')

cause = file['诊断名称'].tolist()
code_nlp = file['算法结果'].tolist()

dic = get_standard_ICD('系统对照表')

for index in range(len(cause)):
    if len(code_nlp[index]) == 7:
        if code_nlp[index][0:5] in dic.keys():
            file_out.write(cause[index] + ',' + code_nlp[index] + ',' + str(dic[code_nlp[index][0:5]]) + '\n')
        else:
            file_out.write(cause[index] + ',' + code_nlp[index] + ',' + '\n')
    elif code_nlp[index] in dic.keys():
        file_out.write(cause[index] + ',' + code_nlp[index] + ',' + str(dic[code_nlp[index]]) + '\n')
    else:
        file_out.write(cause[index] + ',' + code_nlp[index] + ',' + '\n')

file_drop = pd.read_csv(path + '\编码不同的数据对照表.csv', encoding='utf-8')
file_drop = file_drop.drop_duplicates(subset=['CDC诊断名称', '算法结果', '算法结果对应的诊断名称'], keep='first')
file_drop.to_csv(path + '\my_file.csv', encoding='utf-8', index=None)

file_in = codecs.open(path + '\my_file.csv', 'r', encoding='utf-8')
file_out = codecs.open(path + '\\NLP算法结果.csv', 'w', encoding='utf-8')
for line in file_in:
    line = line.strip()
    if line.split(',')[0] != line.split(',')[-1]:
        if '，' not in line.split(',')[0] and ' ' not in line.split(',')[0] and '.' not in line.split(',')[0] and '、' not in line.split(',')[0] and '其他' not in line.split(',')[0] \
                and '其他' not in line.split(',')[1] and '未特指' not in line.split(',')[1] and line.split(',')[0] \
                not in line.split(',')[-1] and line.split(',')[-1] not in line.split(',')[0]:
            file_out.write(line + '\n')




