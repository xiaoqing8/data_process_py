import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def graphic_compare():
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    font_size = 10  # 字体大小
    fig_size = (8, 6)  # 图表大小

    data_name = (u'表的总长度', u'患者总数', u'就诊总数', u'code总数')
    table_name = (u'出院小结', u'诊断表', u'病案诊断表')  # table_name
    data_value = ((34740, 274435, 52984), (19414, 17211, 14955), (25407, 132321, 19934), (0, 5959, 4159))  # data_value

    # 更新字体大小
    mpl.rcParams['font.size'] = font_size
    # 更新图表大小
    mpl.rcParams['figure.figsize'] = fig_size
    # 设置柱形图宽度
    bar_width = 0.2

    index = np.arange(len(data_value))
    # 绘制表的总长度
    rects1 = plt.bar(index, data_value, bar_width, color='#0072BC', label=data_name)
    # 绘制患者总数
    rects2 = plt.bar(index + bar_width, data_value[1], bar_width, color='#ED1C24', label=data_name[1])
    # 绘制就诊总数
    rects3 = plt.bar(index + 2*bar_width, data_value[2], bar_width, color='#00FF00', label=data_name[2])
    # # 绘制code总数
    rects4 = plt.bar(index + 3*bar_width, data_value[3], bar_width, color='#FFA500', label=data_name[3])

    # X轴标题
    plt.xticks(index + bar_width, table_name)
    # Y轴范围
    plt.ylim(ymax=500, ymin=0)
    # 图表标题
    plt.title(u'表数据总结')
    # 图例显示在图表下方
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)
    add_labels(rects1)
    add_labels(rects2)
    add_labels(rects3)
    add_labels(rects4)
    # 图表输出到本地
    plt.savefig(os.getcwd() + '\\figure\\tables review.png')
    plt.show()

# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')


def graphic(data_name, table_name, data_value, title, ymax, savepath, xlable='', ylable=''):
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    font_size = 10  # 字体大小
    fig_size = (8, 6)  # 图表大小

    # data_name = (u'表的总长度', u'患者总数', u'就诊总数', u'code总数')
    # table_name = (u'出院小结', u'诊断表', u'病案诊断表')  # table_name
    # data_value = ((34740, 274435, 52984), (19414, 17211, 14955), (25407, 132321, 19934), (0, 5959, 4159))  # data_value

    # 更新字体大小
    mpl.rcParams['font.size'] = font_size
    # 更新图表大小
    mpl.rcParams['figure.figsize'] = fig_size
    # 设置柱形图宽度
    bar_width = 0.4

    index = np.arange(len(data_value))
    # rects1 = plt.bar(index, data_value, bar_width, color='#0072BC', label=data_name)
    rects1 = plt.bar(index, data_value, bar_width, color='#0072BC')

    # X轴标题
    plt.xticks((index), table_name)
    # Y轴范围
    plt.ylim(ymax=ymax, ymin=0)
    # 图表标题
    plt.title(title)
    # 图例显示在图表下方
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)
    add_labels(rects1)
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    # 图表输出到本地
    # plt.savefig(os.getcwd() + '\\figure\\' + title +'.png')
    plt.savefig(savepath)
    plt.show()