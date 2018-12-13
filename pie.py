from matplotlib import pyplot as plt
import os
import matplotlib as mpl
mpl.use('Agg')
# -*- coding: utf-8 -*-
# labels, size, colors, explode, title需要传参进来，其他部分都是相同的
def pie(labels, sizes, colors, explode, title):

    ## labels = [u'有编码7位', u'有编码6位', u'有编码4位', u'有编码3位', u'无（北京）', u'无（除上海）', u'无（都无）', u'无（全国、国标）', u'无（全国）']  # 定义标签
    # sizes = [2, 19, 7, 5, 7, 3, 5, 3, 1]  # 每块值
    # colors = ['red', 'sienna', 'darkorange', 'darkgoldenrod', 'slategrey', 'purple', 'pink', 'yellowgreen',
    #           'lightskyblue']  # 每块颜色定义
    # explode = (0, 0.02, 0, 0, 0, 0, 0, 0, 0)  # 将某一块分割出来，值越大分割出的间隙越大
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
    plt.figure(figsize=(6, 9))  # 调节图形大小

    patches, text1, text2 = plt.pie(sizes,
                          explode=explode,
                          labels=labels,
                          colors=colors,
                          labeldistance =1.1,  # 图例距圆心半径倍距离
                          autopct ='%3.2f%%',  # 数值保留固定小数位
                          shadow =False,  # 无阴影设置
                          startangle =90,  # 逆时针起始角度设置
                          pctdistance =0.8)  # 数值距圆心半径倍数距离
    # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.legend()
    plt.title(title)
    plt.savefig(os.getcwd() + '\\figure\\' + title + '.png')
    plt.show()

