import codecs
import os
import pandas as pd
import requests
from read_file import get_CDC_ICD, get_standard_ICD
import random

path = os.getcwd()


# 请求顾根的NLP算法API，传入参数诊断名称，得到诊断编码
def post(cause):
    # 访问链接
    target_url = 'http://172.16.0.136:5001/icd'
    content = {"content": cause, "mode": "disease"}
    result = requests.post(target_url, json=content)
    res = result.text.split(',')[0]
    return res


# 只分析每个数据集中最后剩下的不确定的诊断名称-诊断编码对。生成"使用nlp算法生成编码.csv"
# 后面一部分改进是 在全体数据中随机抽样100条数据来看总体的准确度
def nlp_code(file_name):
    # *********************************跑不一致的数据******************************************
    # file_in = pd.read_csv(path + '\编码匹配\\' + file_name + '\编码匹配.csv', encoding='utf-8')
    # cause = file_in['数据集中诊断名称'].tolist()
    # icd = file_in['数据集中诊断编码'].tolist()
    # file = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\使用nlp算法生成编码.csv', 'w', encoding='utf-8')
    # file = codecs.open(path + '\用旧算法跑全部数据\\' + file_name + '\\使用nlp算法生成编码.csv', 'w', encoding='utf-8')
    # file.write('诊断名称,诊断编码,算法结果' + '\n')
    # for index in range(len(cause)):
    #     code = post(cause[index])
    #     file.write(cause[index] + ',' + icd[index] + ',' + code + '\n')

    # ***********************************跑全体数据************************************************
    cause_original, icd_original, _ = get_CDC_ICD(file_name)
    icd = []
    cause = []
    for index in range(len(cause_original)):
        if cause_original[index] != '^' and icd_original[index] != '^':
            cause.append(cause_original[index])
            icd.append(icd_original[index])
    num_code = len(cause)
    # 随机抽样100条
    random_list = random.sample(range(0, len(cause)), 100)

    dic = get_standard_ICD("系统对照表")

    file = codecs.open(path + '\用旧算法跑全部数据\\' + file_name + '\\使用nlp算法生成编码.csv', 'w', encoding='utf-8')
    file.write('诊断名称,诊断编码,诊断编码对应的标准诊断名称,算法结果,算法结果对应的标准诊断名称' + '\n')
    for item in random_list:
        code = post(cause[item])
        if len(code) == 7 and icd[item] in dic.keys() and code[0:5] in dic.keys():
            file.write(cause[item] + ',' + icd[item] + ',' + str(dic[icd[item]]) + ',' + code + ',' + str(dic[code[0:5]]) + '\n')
        elif len(code) == 7 and icd[item] in dic.keys() and code[0:5] not in dic.keys():
            file.write(cause[item] + ',' + icd[item] + ',' + str(dic[icd[item]]) + ',' + code + ',,' + '\n')
        elif code == '0' and icd[item] in dic.keys():
            file.write(cause[item] + ',' + icd[item] + ',' + str(dic[icd[item]]) + ',' + code + ',,' + '\n')
        else:
            file.write(cause[item] + ',' + icd[item] + ',' + str(dic[icd[item]]) + ',' + code + ',' + str(dic[code]) + '\n')
#
# nlp_code('guizhou')
# nlp_code('zhejiang')
# nlp_code('xinjiang')
# nlp_code('beijing')


# 分析生成的nlp结果和原来的CDC编码结果，看看有多少是一位错，二位错，三位错，四位错。以及子节点和父节点的关系
def analysis_nlp(file_name):
    file_in = pd.read_csv(path + '\编码匹配\\' + file_name + '\\nlp\使用nlp算法生成编码.csv', encoding='utf-8')

    cause = file_in['诊断名称'].tolist()
    diag_icd = file_in['诊断编码'].tolist()
    nlp_icd = file_in['算法结果'].tolist()

    file_diff_1 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第一位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_1.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_2 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第二位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_2.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_3 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第三位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_3.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_4 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第X位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_4.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_5 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第四位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_5.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_6 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第五位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_6.write('诊断名称,诊断编码,算法结果' + '\n')
    file_diff_7 = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\第六位编码不同的诊断描述.csv', 'w', encoding='utf-8')
    file_diff_7.write('诊断名称,诊断编码,算法结果' + '\n')

    file_NLP_subset_CDC = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\\NLP给出的编码(三位)是CDC编码（四位）的父节点.csv', 'w', encoding='utf-8')
    file_NLP_subset_CDC.write('诊断名称,诊断编码,算法结果' + '\n')

    file_CDC_subset_ICD = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\\CDC编码是NLP给出的编码的父节点.csv', 'w', encoding='utf-8')
    file_CDC_subset_ICD.write('诊断名称,诊断编码,算法结果' + '\n')

    file_same = codecs.open(path + '\编码匹配\\' + file_name + '\\nlp\\CDC编码和NLP编码完全相同.csv', 'w',encoding='utf-8')
    file_same.write('诊断名称,诊断编码,算法结果' + '\n')

    file_list = [file_diff_1, file_diff_2, file_diff_3, file_diff_4, file_diff_5, file_diff_6, file_diff_7]

    same = 0
    print(len(diag_icd))
    for index in range(len(diag_icd)):
        if diag_icd[index] == nlp_icd[index]:
            same += 1
            file_same.write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
            if same % 5 == 0:
                print('processing......')
        # print(cause[index])
        # print(diag_icd[index])
        # print(nlp_icd[index])
        elif len(diag_icd[index]) == len(nlp_icd[index]):
            for i in range(len(nlp_icd[index])):
                if nlp_icd[index][i] != diag_icd[index][i]:
                    file_list[i].write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
                    break
        elif len(diag_icd[index]) > len(nlp_icd[index]):
            for i in range(len(nlp_icd[index])):
                if nlp_icd[index][i] != diag_icd[index][i]:
                    file_list[i].write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
                    break
                elif i == len(nlp_icd[index]) - 1:
                    file_NLP_subset_CDC.write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
                    break
        elif len(diag_icd[index]) < len(nlp_icd[index]):
            for i in range(len(diag_icd[index])):
                if nlp_icd[index][i] != diag_icd[index][i]:
                    file_list[i].write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
                    break
                elif i == len(diag_icd[index]) - 1:
                    file_CDC_subset_ICD.write(cause[index] + ',' + diag_icd[index] + ',' + nlp_icd[index] + '\n')
                    break
    print("完全相同的code：", same)