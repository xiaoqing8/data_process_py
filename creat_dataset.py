import os
import codecs
import pandas as pd
from read_file import get_CDC_ICD, get_standard_ICD, get_table_length
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import random

path = os.getcwd()


# 统计三张表中出现的所有code的频数，及其所对应的诊断名称的个数，来决定要用到那些code来做训练集。
# code的频数用作：使用出现次数多的code，少的那些不足以训练；频数统计出来之后涉及到lable balance，
# 不能有的标签有一万个训练数据，而有的标签只有几百个训练数据。
# 诊断名称个数涉及到标签学习的可扩展性
# def create_dataset():
#     cause_shanghai, ICD_shanghai, _ = get_CDC_ICD('shanghai')
#     cause_beijing_zhejiang, ICD_beijing_zhejiang, _ = get_CDC_ICD('beijing_zhejiang')
#     cause_guizhou_xinjiang, ICD_guizhou_xinjiang, _ = get_CDC_ICD('guizhou_xinjiang')
#
#     cause = []
#     icd = []
#
#     cause_list = [cause_shanghai, cause_beijing_zhejiang, cause_guizhou_xinjiang]
#     icd_list = [ICD_shanghai, ICD_beijing_zhejiang, ICD_guizhou_xinjiang]
#
#     for index in range(len(cause_list)):
#         for index_inner in range(len(cause_list[index])):
#             if cause_list[index][index_inner] != '^' and icd_list[index][index_inner] != '^' and icd_list[index][index_inner][0].encode('utf-8').isalpha():
#                 cause.append(cause_list[index][index_inner])
#                 icd.append(icd_list[index][index_inner])
#
#     # 将每个code被编过的诊断描述统计出来
#     dict = {}
#     for i in range(len(cause)):
#         if icd[i] in dict.keys():
#             if cause[i] not in dict[icd[i]]:
#                 dict[icd[i]].append(cause[i])
#         else:
#             dict[icd[i]] = []
#             dict[icd[i]].append(cause[i])
#     #  三个数据集一共涉及到6761个code
#
#     # 统计每个code出现的频数
#     dic = {}
#     for num in icd:
#         if num in dic.keys():
#             dic[str(num)] += 1
#         else:
#             dic[str(num)] = 1
#
#     sort_code = sorted(dic.items(), key=lambda d: d[1], reverse=True)
#
#     file_out = codecs.open(path + '\dataset\code_diag_frequence.txt', "w", encoding='utf-8')
#     file_out_len = codecs.open(path + '\dataset\code_len(diag)_frequence.txt', "w", encoding='utf-8')
#
#     for v in sort_code:
#         file_out.write(str(v[0]) + '\t' + str(dict[v[0]]) + '\t' + str(v[1]) + '\n')
#         file_out_len.write(str(v[0]) + '\t' + str(len(dict[v[0]])) + '\t' + str(v[1]) + '\n')
#     file_out.close()
#
#     # 上面是做好了code的频数统计，下面可基于上面的成果来做训练集。
#     # 以code出现的频率为基准，如果我们假设要在每个code下
#     # 选择30000个作为训练集+测试集，那么在icd中找到这个code,并且对应到cause[index],
#     # 然后随机选出30000个icd-cause对作为我们的训练集中的数据。
#     # 在此过程中按照8:2的准则分配到train和test
# create_dataset()


def create_dataset():
    cause_shanghai, ICD_shanghai, _ = get_CDC_ICD('shanghai')
#     cause_beijing_zhejiang, ICD_beijing_zhejiang, _ = get_CDC_ICD('beijing_zhejiang')
#     cause_guizhou_xinjiang, ICD_guizhou_xinjiang, _ = get_CDC_ICD('guizhou_xinjiang')
#
#     cause = []
#     icd = []
#
#     cause_list = [cause_shanghai, cause_beijing_zhejiang, cause_guizhou_xinjiang]
#     icd_list = [ICD_shanghai, ICD_beijing_zhejiang, ICD_guizhou_xinjiang]
#
#     for index in range(len(cause_list)):
#         for index_inner in range(len(cause_list[index])):
#             if cause_list[index][index_inner] != '^' and icd_list[index][index_inner] != '^' and icd_list[index][index_inner][0].encode('utf-8').isalpha():
#                 cause.append(cause_list[index][index_inner])
#                 icd.append(icd_list[index][index_inner])
#
#     print(len(icd))
#
#     dic = get_standard_ICD("系统对照表")
#
#     file_out = codecs.open(path + '\dataset\data.txt', "w", encoding='utf-8')
#
#     file_diff = codecs.open(path + '\dataset\除去完全匹配的数据.csv', "w", encoding='utf-8')
#     file_diff.write('CDC诊断名称,CDC诊断编码' + '\n')
#
#     file_frequence = codecs.open(path + '\dataset\频数统计除去完全匹配的数据.csv', "w", encoding='utf-8')
#     file_frequence.write('CDC诊断名称,CDC诊断编码' + '\n')
#
#     for index in range(len(cause)):
#         if icd[index].upper() in dic.keys():
#             for i in dic[icd[index].upper()]:
#                 if i == cause[index]:
#                     file_out.write(cause[index] + '\t' + icd[index] + '\n')
#                 else:
#                     file_diff.write(cause[index] + ',' + icd[index] + '\n')
#
#     file_fre = pd.read_csv(path + '\dataset\除去完全匹配的数据.csv', encoding='utf-8')
#     cause_diff = file_fre['CDC诊断名称']
#     code_diff = file_fre['CDC诊断编码']
#     diff_list = []
#     for index in range(len(cause_diff)):
#         diff_list.append(cause_diff[index] + '@' + code_diff[index])
#
#     dic_fre = {}
#     for i in diff_list:
#         if i in dic_fre.keys():
#             dic_fre[i] += 1
#         else:
#             dic_fre[i] = 1
#
#     sort_code = sorted(dic_fre.items(), key=lambda d: d[1], reverse=True)
#
#     for value in sort_code:
#         file_frequence.write(str(value) + '\n')
#
#     file_out.close()
#     # 上面是做好了code的频数统计，下面可基于上面的成果来做训练集。
#     # 以code出现的频率为基准，如果我们假设要在每个code下
#     # 选择30000个作为训练集+测试集，那么在icd中找到这个code,并且对应到cause[index],
#     # 然后随机选出30000个icd-cause对作为我们的训练集中的数据。
#     # 在此过程中按照8:2的准则分配到train和test


def statistic_data():
    file_in = codecs.open(path + '\dataset\data.txt', 'r', encoding='utf-8')
#     cause_dedup = set()
#     code_dedup = set()
#     cause = []
#     code = []
#     for line in file_in:
#         line = line.strip()
#         cause.append(line.split('\t')[0])
#         code.append(line.split('\t')[1])
#         cause_dedup.add(line.split('\t')[0])
#         code_dedup.add(line.split('\t')[1])
#     print(len(cause_dedup), len(code_dedup), len(cause), len(code), len(set(cause)), len(set(code)))
#
#     dic = {}
#     for i in code:
#         if i in dic.keys():
#             dic[i] += 1
#         else:
#             dic[i] = 1
#
#     dict = {}
#     for index in range(len(cause)):
#         if cause[index] in dict.keys():
#             if code[index] not in dict[cause[index]]:
#                 dict[cause[index]].append(code[index])
#         else:
#             dict[cause[index]] = []
#             dict[cause[index]].append(code[index])
#
#     for key, value in dict.items():
#         if len(value) > 1:
#             print(key, value)
#
#     file_out = codecs.open(path + '\dataset\完全匹配的数据频数统计.txt', 'w', encoding='utf-8')
#     sort_code = sorted(dic.items(), key=lambda d: d[1], reverse=True)
#
#     for value in sort_code:
#         file_out.write(str(value) + '\n')
# statistic_data()


# 得到各个地区的诊断名称
def diag(file_name):
    table, _ = get_table_length(file_name)
    table = table.fillna(value='^')
    file = table[['CARDID', 'A_CAUSE', 'B_CAUSE', 'C_CAUSE', 'D_CAUSE', 'OTHER1_CAUSE', 'BASECAUSE']]
    file.to_csv(path + '\\dataset\各地区死因总表\\' + file_name + '_死因总表.csv', encoding='utf-8', index=None)


# 将各地区的诊断名称都集合
def combine_diag():
    diag('guizhou')
    diag('shanghai')
    diag('xinjiang')
    diag('zhejiang')
    diag('beijing')


# 将所有地区的诊断名称和调查报告整合在一起
def combine_death_report():
    file_report = pd.read_csv(path + '\dataset\不为空的调查报告.csv', encoding='utf-8')
    id_report = file_report['CARDID'].tolist()
    content_report = file_report['report'].tolist()

    print(len(id_report))
    print(id_report[0])
    dic_report = {}
    for index in range(len(id_report)):
        dic_report[id_report[index]] = content_report[index]

    file_death_reason = codecs.open(path + '\dataset\死因总表.csv', 'r', encoding='utf-8')
    file_out = codecs.open(path + '\dataset\整合调查报告和死因总表.csv', 'w', encoding='utf-8')
    file_out.write('CARDID,A_CAUSE,B_CAUSE,C_CAUSE,D_CAUSE,OTHER1_CAUSE,BASECAUSE,report' + '\n')

    count = 0
    for line in file_death_reason:
        line = line.strip()
        if line.split(',')[0] in dic_report.keys():
            count += 1
            # print(dic_report[line.split(',')[0]])
            file_out.write(line + ',' + dic_report[line.split(',')[0]] + '\n')
        else:
            file_out.write(line + ',' + '\n')
    print('能匹配到report的CARDID总数：', count)
# combine_death_report()


def extract_sample(extract_list):
    table = pd.read_csv(path + '\dataset\整合调查报告和死因总表.csv', encoding='utf-8')
    extract_content = table[extract_list]

    header = extract_list
    extract_content.to_csv(path + '\dataset\数据集的输入.csv', encoding='utf-8', index=None, header=header)


def extract_base():
    table = pd.read_csv(path + '\dataset\整合调查报告和死因总表.csv', encoding='utf-8')
    base = table['BASECAUSE']
    header = 'BASECAUSE'
    base.to_csv(path + '\dataset\数据集的标签.csv', encoding='utf-8', index=None, header=header)


def get_dataset():
    file_in = codecs.open(path + '\dataset\数据集的输入.csv', 'r', encoding='utf-8')
    file_lable = codecs.open(path + '\dataset\数据集的标签.csv', 'r', encoding='utf-8')

    file_dataset = codecs.open(path + '\dataset\数据集.csv', 'w', encoding='utf-8')

    in_list = file_in.readlines()
    lable_list = file_lable.readlines()

    count = 0
    not_vide = 0

    for index in range(1, len(in_list)):
        # 只将根本死因不为空的数据加入到数据集中。
        if lable_list[index].strip() != '^':
            if in_list[index].strip().split(',')[-1] != '':
                count += 1
            value = in_list[index].strip().replace('^,', '')
            if value[-1] == ',':
                value = value[:-1]
            file_dataset.write(value + ' @ ' + lable_list[index].strip() + '\n')
        if in_list[index].strip().split(',')[-1] != '':
            not_vide += 1
    print(not_vide)
    print(count)
    # print(in_list[1].strip().split(',')[-1] == '')


def cause_group():
    dic = {}
    not_blanc_list = []

    # 全体死因链数据中A,B,C,D各种组合的比例      全体死因链根本死因不为空的数据中各种组合的比例用的table
    # table = pd.read_csv(path + '\dataset\死因总表.csv', encoding='utf-8')

    table = pd.read_csv(path + '\dataset\数据集的输入.csv', encoding='utf-8')
    table = table.fillna(value='^')

    a_c = table['A_CAUSE'].tolist()
    b_c = table['B_CAUSE'].tolist()
    c_c = table['C_CAUSE'].tolist()
    d_c = table['D_CAUSE'].tolist()
    other_c = table['OTHER1_CAUSE'].tolist()

    report = table['report'].tolist()

    # base_c = table['BASECAUSE'].tolist()

    data_list = [a_c, b_c, c_c, d_c]
    list_name = ['a_c', 'b_c', 'c_c', 'd_c', 'other_c', 'base_c']

    # # # *****************************考察A B C D的多种组合****************************
    # for index in range(len(a_c)):
    #     for i in range(len(data_list)):
    #         if data_list[i][index] != '^':
    #             not_blanc_list.append(list_name[i])
    #     if str(not_blanc_list) in dic.keys():
    #         dic[str(not_blanc_list)] += 1
    #     else:
    #         dic[str(not_blanc_list)] = 1
    #     not_blanc_list = []

    # # # **********************考察A B C D的多种组合， 在base不为空的情况下**************************
    # for index in range(len(a_c)):
    #     for i in range(len(data_list)):
    #         if base_c[index] != '^':
    #             if data_list[i][index] != '^':
    #                 not_blanc_list.append(list_name[i])
    #     if str(not_blanc_list) in dic.keys():
    #         dic[str(not_blanc_list)] += 1
    #     else:
    #         dic[str(not_blanc_list)] = 1
    #     not_blanc_list = []

    # # **********************考察A B C D的多种组合， 在有report的情况下**************************
    yxq_count = 0
    for index in range(len(a_c)):
        if report[index] != '^':
            yxq_count += 1
            for i in range(len(data_list)):
                if data_list[i][index] != '^':
                    not_blanc_list.append(list_name[i])
        if str(not_blanc_list) in dic.keys():
            dic[str(not_blanc_list)] += 1
        else:
            dic[str(not_blanc_list)] = 1
        not_blanc_list = []
    print(yxq_count)
    # file_out = codecs.open(path + '\dataset\数据分析mhd\全体A B C D的cause的组合.txt', 'w', encoding='utf-8')
    # file_out = codecs.open(path + '\dataset\数据分析mhd\根本死因不为空的数据中A B C D的cause的组合.txt', 'w', encoding='utf-8')
    file_out = codecs.open(path + '\dataset\数据分析mhd\有调查报告的数据中各种组合.txt', 'w', encoding='utf-8')
    sum = 0
    for key, value in dic.items():
        file_out.write(key + ' ' + str(value) + '\n')
        sum += value
    print(sum)


def len_text():
    file_in = codecs.open(path + '\dataset\数据集.csv', 'r', encoding='utf-8')

    length_list_in = []
    length_list_out = []

    for line in file_in:
        line = line.strip()
        length_list_in.append(len(line.split(' @ ')[0]))
        length_list_out.append(len(line.split(' @ ')[1]))
    data = pd.DataFrame({"数据集中输入的长度": length_list_in,
                         "数据集中输出的长度": length_list_out})

    print(data.describe())
    # print(data.var())
    print(sum(length_list_in)/len(length_list_in))
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    font_size = 10  # 字体大小
    fig_size = (8, 6)  # 图表大小
    # 更新字体大小
    mpl.rcParams['font.size'] = font_size
    # 更新图表大小
    mpl.rcParams['figure.figsize'] = fig_size

    data.plot(kind='box', notch=True, grid=True)
    plt.ylabel("长度分布")
    plt.xlabel("数据集")  # 我们设置横纵坐标的标题。
    plt.savefig(path + '\dataset\数据分析mhd\箱型图.jpg')
    plt.show()


def random_sample():
    file_in = codecs.open(path + '\dataset\排序_输入输出相似度.txt', 'r', encoding='utf-8')
    file_out_without = codecs.open(path + '\dataset\数据分析mhd\没有report.txt', 'w', encoding='utf-8')
    file_out_with = codecs.open(path + '\dataset\数据分析mhd\有report.txt', 'w', encoding='utf-8')
    list = file_in.readlines()

    random_list = random.sample(range(55000, 100000), 20)
    print(random_list)
    for index in random_list:
        file_out_without.write(list[index] + '\n')

    random_list = random.sample(range(180000, 192711), 20)
    print(random_list)
    for index in random_list:
        file_out_with.write(list[index] + '\n')


if __name__ == '__main__':
    # combine_diag()
    # combine_death_report()

    # #抽取数据集的输入和输出
    # extract_list = ['A_CAUSE','B_CAUSE','C_CAUSE','D_CAUSE','OTHER1_CAUSE','report']
    # extract_sample(extract_list)
    # extract_base()

    # get_dataset()

    # file = codecs.open(path + '\death17_调查记录_全国.csv', 'r', encoding='utf-8')
    # for line in file:
    #     if '1fd56bc2-fd54-4df6-a780-66c34b2632f0' in line:
    #         print(1111, line)
    #         break

    # cause_group()

    # len_text()
    random_sample()
