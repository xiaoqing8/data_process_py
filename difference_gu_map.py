import codecs
import os
import pandas as pd
from read_file import get_CDC_ICD


# 得到顾根的ICD表中没有的 CDC数据中的code
def get_difference_code(file_name):
    path = os.getcwd()
    # 得到要用到的icd标准文件
    file = pd.read_csv(path + '\data\icd10.csv', encoding='utf-8')
    # 从文件中得到编码一列
    ICD_original = file['code'].tolist()

    # 将ICD_original中的数据第一位大写后重新写入到ICD_reference列表中
    ICD_reference = []
    for value in ICD_original:
        value = value.upper()
        ICD_reference.append(value)

    # 得到上海或者某个地区的ICD list, 并将其去重后存入到new_icd中
    _, icd_cdc_original, _ = get_CDC_ICD(file_name)
    icd_cdc = []
    for item in icd_cdc_original:
        if item != '^':
            icd_cdc.append(item.upper())
    new_icd = set(icd_cdc)

    #  遍历new_icd列表中的元素，看其是否在ICD_referencez中，把不在这个列表中的元素写入到文件'not exist.txt'
    file_out = codecs.open(path + '\\not exist\\not exist ' + file_name + '.txt', 'w', encoding='utf-8')
    for v in new_icd:
        if v not in ICD_reference and (len(v) == 3 or len(v) == 5) and v[0].encode('utf-8').isalpha():
            if v == '冠状动':
                print(v[0].isalpha())
            file_out.write(v + '\n')
    file_out.close()


# 算三个文件的code列表的并集
def combine():
    path = os.getcwd()
    # 把三个文件中的code都抽成list
    list_1 = []
    list_2 = []
    list_3 = []
    list = [list_1, list_2, list_3]
    file_1 = codecs.open(path + '\\not exist\\not exist shanghai.txt', 'r', encoding='utf-8')
    file_2 = codecs.open(path + '\\not exist\\not exist beijing_zhejiang.txt', 'r', encoding='utf-8')
    file_3 = codecs.open(path + '\\not exist\\not exist guizhou_xinjiang.txt', 'r', encoding='utf-8')
    file_list = [file_1, file_2, file_3]
    for index in range(len(file_list)):
        for line in file_list[index]:
            line = line.strip()
            list[index].append(line)
    for file in file_list:
        file.close()
    # print(len(list_1), len(list_2), len(list_3))
    # 对三个list取并集得到全部数据集中在顾根的表中不存在的code，并写入文件not exist union
    union_list = set(list_1).union(set(list_2)).union(set(list_3))
    print(len(union_list))
    file_union = codecs.open(path + '\\not exist\\not exist union.txt', 'w', encoding='utf-8')
    for i in union_list:
        file_union.write(i + '\n')
    file_union.close()


get_difference_code('beijing_zhejiang')
get_difference_code('guizhou_xinjiang')
get_difference_code('shanghai')
combine()
