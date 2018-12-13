from histogram import graphic
import codecs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from interval import Interval

file = codecs.open("D:\stage\data_process_系统对照表\dataset\排序_输入输出相似度.txt", 'r', encoding='utf-8')
prob = []
for line in file:
    line = line.strip()
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

inter = [Interval(0.1, 0.5), Interval(0.5, 0.6), Interval(0.6, 0.7), Interval(0.7, 0.8), Interval(0.8, 0.9), Interval(0.9, 1)]
lis = [one, two, three, four, five, six]
for item in prob:
    for index in range(len(inter)):
        if item in inter[index]:
            lis[index] += 1

axis = ['<0.5', '0.5-0.6', '0.6-0.7', '0.7-0.8', '0.8-0.9', '0.9-1']
yxis = lis
print(lis)

f = plt.figure(2)
plt.bar(axis, yxis, 0.3, color="green")
plt.show()
plt.savefig("D:\stage\data_process_系统对照表\dataset\数据分析mhd\概率柱状图.jpg")

