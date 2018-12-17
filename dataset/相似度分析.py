from histogram import graphic
import codecs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from interval import Interval
import random

file = codecs.open("D:\stage\data_process_系统对照表\dataset\排序_输入输出相似度.txt", 'r', encoding='utf-8')
file_out = codecs.open("D:\stage\data_process_系统对照表\dataset\抽样相似度表.txt", 'w', encoding='utf-8')

prob = []
lines = []

for line in file:
    line = line.strip()
    lines.append(line)
    line = line.split(' ### ')
    prob.append(float(line[1]))

# ************prob分布
# count       192711
# mean        0.719646
# std         0.160318
# min         0.194080
# 25%         0.592099
# 50%         0.720519
# 75%         0.851094
# max         1.000000

# f1 = plt.figure(1)
# # plt.scatter(range(len(prob)), prob, s=0.1)
# plt.plot(range(len(prob)), prob, "r", linewidth=1)
# plt.savefig("D:\stage\data_process_系统对照表\dataset\数据分析mhd\概率散点图.jpg")
# plt.show()


one = 0
two = 0
three = 0
four = 0
five = 0
six = 0

# inter = [Interval(0.1, 0.5), Interval(0.5, 0.6), Interval(0.6, 0.7), Interval(0.7, 0.8), Interval(0.8, 0.9), Interval(0.9, 1)]
# lis = [one, two, three, four, five, six]
inter = [Interval(0.9, 1), Interval(0.8, 0.9), Interval(0.7, 0.8),Interval(0.6, 0.7), Interval(0.5, 0.6), Interval(0.1, 0.5)]
lis = [six, five, four, three, two, one]
for item in prob:
    for index in range(len(inter)):
        if item in inter[index]:
            lis[index] += 1

axis = ['<0.5', '0.5-0.6', '0.6-0.7', '0.7-0.8', '0.8-0.9', '0.9-1']
yxis = lis
print(lis)

lis_1 = lis_2 = lis_3 = lis_4 = lis_5 = lis_6 = []
lis_sample = [lis_1, lis_2, lis_3, lis_4, lis_5, lis_6]
for index in range(len(lis_sample)):
    if index == 0:
        lis_sample[index] = random.sample(range(0, lis[0]), 20)
    elif index == 5:
        lis_sample[index] = random.sample(range(sum(lis)-lis[-1]+1, sum(lis)), 40)
    else:
        lis_sample[index] = random.sample(range(sum(lis[0:index])-1, sum(lis[0:index+1])), 20)


for i in lis_sample:
    print(i)

print(8888, len(lines))
for list_name in lis_sample:
    for num in list_name:
        file_out.write(lines[num].replace(' ### ', '\t') + '\n')

file.close()
file_out.close()
# f = plt.figure(2)
# plt.bar(axis, yxis, 0.3, color="green")
# plt.show()
# plt.savefig("D:\stage\data_process_系统对照表\dataset\数据分析mhd\概率柱状图.jpg")

