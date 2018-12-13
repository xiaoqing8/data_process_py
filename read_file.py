from sas7bdat import SAS7BDAT
import codecs
import os
import pandas as pd
import xlrd
from similarity import similarity
# from pie import pie
# from histogram import graphic_compare
from histogram import graphic
import matplotlib.pyplot as plt
import numpy as np
from urllib import request, parse
import requests
import time
import random

path = os.getcwd()
# requests.adapters.DEFAULT_RETRIES = 511
s = requests.session()
s.keep_alive = False


# 将7sasdbat文件转换成CSV文件
def get_file(file_name):
    if not os.path.exists(path + '\data\\' + file_name +'.csv'):
        with SAS7BDAT(path + '\data\\' + file_name + '.sas7bdat', encoding='gb2312') as file:
            df = file.to_data_frame()
        df.to_csv(path + '\data\\' + file_name +'.csv', index=None)


# 将目标CSV文件读成DataFrame,并返回表长
def get_table_length(file_name):
    file_in = pd.read_csv(path + "\data\\" + file_name + ".csv", encoding='utf-8')
    table_length = len(file_in)
    file_in[['PATIENTNAME', 'ADDR', 'REGISTERADDR', 'FOLKNAME', 'FOLKTEL', 'FOLKADDR', 'INFORMANT', 'RELATIONSHIP', 'INFORMANTADDR', 'INFORMANTTEL', 'INVESTIGATOR', 'USERID', 'AUDIT_USER']] = ''
    file_in.to_csv(path + '\data\\' + file_name +'.csv', index=None)
    # print(88888888, table_length)
    return file_in, table_length
# get_table_length('guizhou_xinjiang')


# 表的整体数据统计分析
def describe(file_name):
    table, _ = get_table_length(file_name)
    info_table = table.info()
    distribution_table = table.describe()
    category_dis = table.describe(include=['O'])
    print(info_table)
    print('_' * 40)
    # print(distribution_table)
    print('_' * 40)
    # print(category_dis)
# describe()


# 得到表的所有表头名字
def get_column_name(file_name):
    table, _ = get_table_length(file_name)
    names = table.columns.values
    # 得到表头内容以及表头长度
    print(names)
    print(len(names))  # 91
    return names, len(names)


# 将表头英文兑换成英文
def eng_to_chi():
    xls_file = xlrd.open_workbook(path + "\data\变量名列表.xls")
    xls_sheet = xls_file.sheets()[0]
    col_chi = xls_sheet.col_values(1)
    col_eng = xls_sheet.col_values(2)
    # 构建中英文索引表
    dic = {}
    for index in range(len(col_eng)):
        dic[col_eng[index]] = col_chi[index]

    names, _ = get_column_name()
    string = ""
    for value in names:
        if value in dic.keys():
            string = string + dic[value] + ","
        else:
            string = string + value + ","
    print(string)
    return string


# 将表中缺失值用'^'替换并返回需要的某一列,list
def get_one_column(file_name, table_name):
    table, _ = get_table_length(file_name)
    table = table.fillna(value='^')
    temp = table[table_name].tolist()
    return temp


# 统计card_id的数据信息
def card_id(file_name):
    table, _ = get_table_length(file_name)
    table = table.fillna(value='^')
    card_id = table['CARDID'].tolist()
    # print(set(card_id))
    count_card_id = 0
    list_card_id = []
    for value in card_id:
        if value == '^':
            count_card_id += 1
        else:
            list_card_id.append(value)
    print("card_id的个数：", len(set(list_card_id)))
    # 1223 2464 13731 55093 76030行没有card_ID
    print('card_id为空的数目统计：', count_card_id)


# 统计死亡人群类型
def personal_type(file_name):
    table, _ = get_table_length(file_name)
    table = table.fillna(value='^')
    temp = table['PERSONAL_TYPE'].tolist()
    print(set(temp))
    count_women_type = 0
    count_child = 0
    count_other = 0
    for value in temp:
        if value == '孕产妇':
            count_women_type += 1
        elif value == '五岁以下' or value == '5岁以下儿童':
            count_child += 1
        elif value == '其他人群':
            count_other += 1
    print(count_women_type, count_child, count_other)  # 29, 230, 85084

    data_name = (u'personal_type')
    table_name = ('孕产妇', '儿童', '其他人群 85084', '缺失值')  # table_name
    title = 'personal_type'
    data_value = (count_women_type, count_child, count_other, 85370-count_women_type-count_child-count_other)  # data_value
    graphic(data_name, table_name, data_value, title, 85000)
    return count_women_type, count_child, count_other


# 得到证件类型并返回每个证件的个数
def get_card_type(file_name):
    lis = get_one_column(file_name, 'IDCARD_TYPE')
    count_ID = 0
    count_officier = 0
    count_taiwan = 0
    count_passport = 0
    count_other = 0
    count_gangao = 0
    count_rigister = 0
    count = 0
    for v in lis:
        if v == '身份证':
            count_ID += 1
        elif v == '军官证':
            count_officier += 1
        elif v == '台湾通行证':
            count_taiwan += 1
        elif v == '护照':
            count_passport += 1
        elif v == '其他法' or v == '其他法定有效证件':
            count_other += 1
        elif v == '港澳通行证':
            count_gangao += 1
        elif v == '户口簿':
            count_rigister += 1
        elif v == '^':
            count += 1
    return count, count_ID, count_officier, count_taiwan, count_passport, count_other, count_gangao, count_rigister


# 统计身份证号.并看一下有没有重复的值
def get_ID(file_name):
    id_list = get_one_column(file_name, 'ID')
    lis = []
    for value in id_list:
        if value != '^':
            lis.append(value)
    print(len(lis))
    print(len(set(lis)))
    if len(lis) == len(set(lis)):
        return True
    else:
        return False


# 统计身份证件号有没有错误,并将其他证件类型及个数输出
def checkout_ID(file_name):
    card_type = get_one_column(file_name, 'IDCARD_TYPE')
    id = get_one_column(file_name, 'ID')
    count_error = 0
    file = codecs.open(path + '\\result\\' + file_name + '\身份证位数存在错误的例子.txt', 'w', encoding='utf-8')
    file_other_card_type = codecs.open(path + '\\result\\' + file_name + '\除身份证外的其他证件类型及号码.txt', 'w', encoding='utf-8')
    for index in range(len(card_type)):
        if card_type[index] == '身份证':
            if id[index] != ['^'] and len(id[index]) != 18 and len(id[index] != 15):
                count_error += 1
                file.write(card_type[index] + ' ' + id[index] + '\n')
        elif card_type[index] != '^':
            file_other_card_type.write(card_type[index] + ' ' + id[index] + '\n')
    print(count_error)


# 出生日期与身份证上的出生日期进行对比,看看有没有身份证上的出生日期与记录的出生日期不符合的信息
def birthday_ID(file_name):
    file = codecs.open(path + '\\result\\' + file_name + '\ID_BIRTHDAY.txt', 'w', encoding='utf-8')
    birthday = get_one_column(file_name, 'BIRTHDAY')
    id = get_one_column(file_name, 'ID')
    count_diff = 0
    all_exist = 0
    diff = []
    for index in range(len(birthday)):
        if birthday[index] != '^' and id[index] != '^' and len(id[index]) == 18:
            all_exist += 1
            if id[index][6:14] != birthday[index].replace('-', ''):
                count_diff += 1
                file.write(id[index][6:14] + ' ' + birthday[index].replace('-', '') + '\n')
                # diff.append(id[index][6:14] + ' ' + birthday[index].replace('-', ''))
        elif birthday[index] != '^' and id[index] != '^' and len(id[index]) == 15:
            all_exist += 1
            if id[index][6:12] != birthday[index].replace('-', '')[2:]:
                count_diff += 1
                file.write(id[index][6:14] + ' ' + birthday[index].replace('-', '') + '\n')
                # diff.append(id[index][6:14] + ' ' + birthday[index].replace('-', ''))
    # print(diff)
    print(11111, count_diff, all_exist)


# 得到民族的分布
def nationname(file_name):
    nationname = get_one_column(file_name, 'NATIONNAME')
    count_unknown = 0
    count_han = 0
    count_minority = 0
    for value in nationname:
        if value == '不详':
            count_unknown += 1
        elif value == '汉族':
            count_han += 1
        else:
            count_minority += 1
    print(count_unknown, count_han, count_minority)
    return count_unknown, count_han, count_minority
# nationname()


# 得到maybecase的一些信息，将A B C D and other cause和maybeccase写入到一个文件进行对比
def maybe_case(file_name):
    a = get_one_column(file_name, 'A_CAUSE')
    b = get_one_column(file_name, 'B_CAUSE')
    c = get_one_column(file_name,'C_CAUSE')
    d = get_one_column(file_name, 'D_CAUSE')
    other = get_one_column(file_name, 'OTHER1_CAUSE')
    base = get_one_column(file_name,'BASECAUSE')
    maybe = get_one_column(file_name,'MAYBE_CASE')
    file = codecs.open(path + '\\result\\' + file_name + '\maybecase.csv', 'w', encoding='utf-8')
    file.write('A_CAUSE,B_CAUSE,C_CAUSE,D_CAUSE,OTHER1_CAUSE,BASECAUSE,MAYBE_CASE' + '\n')

    for index in range(len(maybe)):
        if maybe[index] != '^':
            file.write(a[index] + ',' + b[index] + ',' + c[index] + ',' + d[index] + ',' + other[index] + ',' + base[index] + ',' + maybe[index] + '\n')

    # 统计maybe_case中的字数
    count = 0
    for value in maybe:
        if len(value) != 3 and value != '^':
            count += 1
            print(value)
    print('长度不为3的maybe_case的统计: ', count)  # 长度不为3的maybe_case的统计


# 由诊断编码判断根本死因与哪一次的诊断一样，将与abcd other都不一样的诊断编码-诊断描述对写入到文件“与给出的编码都不一样的根本死因编码”。
# 最后统计编码的位数，是三位码还是四位码
def base_abcd_match(file_name):
    card_id = get_one_column(file_name, 'CARDID')
    a = get_one_column(file_name, 'A_ICD10')
    a_c = get_one_column(file_name, 'A_CAUSE')
    b = get_one_column(file_name, 'B_ICD10')
    b_c = get_one_column(file_name, 'B_CAUSE')
    c = get_one_column(file_name, 'C_ICD10')
    c_c = get_one_column(file_name, 'C_CAUSE')
    d = get_one_column(file_name, 'D_ICD10')
    d_c = get_one_column(file_name, 'D_CAUSE')
    other = get_one_column(file_name, 'OTHER1_ICD10')
    other_c = get_one_column(file_name, 'OTHER1_CAUSE')
    base = get_one_column(file_name, 'BSICD10')
    base_c = get_one_column(file_name, 'BASECAUSE')

    # print(222222222222, len(a), len(a_c), len(b), len(b_c))
    # 得到根本死因与哪一次诊断最相关
    A = 0
    B = 0
    C = 0
    D = 0
    OTHER = 0
    dif = 0

    file = codecs.open(path + '\\result\\' + file_name + '\与给出的编码都不一样的根本死因编码.csv', 'w', encoding='utf-8')
    for index in range(len(base)):
        if base[index] == a[index]:
            A += 1
        if base[index] == b[index]:
            B += 1
        if base[index] == c[index]:
            C += 1
        if base[index] == d[index]:
            D += 1
        if base[index] == other[index]:
            OTHER += 1
        if base[index] != other[index] and base[index] != d[index] and base[index] != c[index] and base[index] != b[index] and base[index] != a[index]:
            dif += 1
            file.write(card_id[index] + ',' + a_c[index] + ',' + a[index] + ',' + b_c[index] + ', ' + b[index] + ',' + c_c[index] + ',' + c[index] + ',' + d_c[index] + ',' + d[index] + ',' + other_c[index] + ',' + other[index] + ',' + base_c[index] + ',' + base[index] + '\n')
    print(A, B, C, D, OTHER, dif)  # 42510 28313 10442 2813 24 1268
    data_name = (u'与A B C D 或者 other code相同的根本死因编码')
    table_name = ('A', 'B', 'C', 'D', 'other', '都不相同')  # table_name
    title = '与A B C D 或者 other code相同的根本死因编码'
    data_value = (A, B, C, D, OTHER, dif)  # data_value
    path_1 = os.getcwd() + '\\figure\\' + file_name + '\与A B C D 或者 other code相同的根本死因编码.png'
    graphic(data_name, table_name, data_value, title, 1600, path_1)

    data_name = ('A B C D OTHER编码分别对得到根本死因编码的有用性')
    table_name = (u'A', u'B', u'C', u'D', u'其他编码')  # table_name
    title = 'A B C D OTHER编码分别对得到根本死因编码的有用性'
    data_value = (round(A/85363, 3), round(B/48366, 3), round(C/16751, 3), round(D/3952, 3), round(OTHER/44891, 3))
    path_2 = os.getcwd() + '\\figure\\' + file_name + '\A B C D OTHER编码分别对得到根本死因编码的有用性.png'
    graphic(data_name, table_name, data_value, title, 0.8, path_2)
    #  ICD编码的位数统计
    # three = 0
    # four = 0
    # five = 0
    # six = 0
    # better = 0
    # for combine in [a, b, c, d, other, base]:
    #     for i in combine:
    #         if len(i) == 3:
    #             three += 1
    #         if len(i) == 4:
    #             four += 1
    #         if len(i) == 5:
    #             five += 1
    #         if len(i) == 6:
    #             six += 1
    #         if len(i) > 6:
    #             better += 1
    # print(three, four, five, six, better)
    return a_c, a, b_c, b, c_c, c, d_c, d, other_c, other, base_c, base


# 得到死因链数据，包括每次的诊断名称、诊断编码以及根本死因及其编码。写入到文件死因_ICD_总表
def abcdBase_table(file_name):
    table, _ = get_table_length(file_name)
    table = table.fillna(value='^')
    sum = table[['CARDID', 'A_CAUSE', 'A_ICD10', 'B_CAUSE', 'B_ICD10', 'C_CAUSE', 'C_ICD10', 'D_CAUSE', 'D_ICD10',  'OTHER1_CAUSE', 'OTHER1_ICD10', 'BASECAUSE', 'BSICD10']]
    sum.to_csv(path + '\\result\\' + file_name + '\死因_ICD_总表.csv', encoding='utf-8', index=None)


# 查看与根本死因不同的再编码code
def rcoder(file_name):
    card_id = get_one_column(file_name, 'CARDID')
    base_icd = get_one_column(file_name, 'BSICD10')
    icd = get_one_column(file_name, 'icd')
    file_error = codecs.open(path + '\\result\\' + file_name + '\根本死因与再编码死因不一样的实例.csv', 'w', encoding='utf-8')
    file_error.write("cardID,根本死因编码,再编码编码")

    count_ICD = 0
    for index in range(len(base_icd)):
        if base_icd[index] == icd[index]:
            count_ICD += 1   # 85369
        else:
            file_error.write(card_id[index] + ',' + base_icd[index] + ',' + icd[index])
    print('根本死因与再编码死因不一样的实例数：', count_ICD)
    return count_ICD


def age(file_name):
    age = get_one_column(file_name, 'age')
    a = 0  # 0-5
    b = 0  # 5-20
    c = 0  # 20-40
    d = 0  # 40-60
    e = 0  # 60-80
    f = 0  # 80-100
    g = 0
    for value in age:
        if value > 0 and value < 5:
            a += 1
        elif value > 5 and value < 20:
            b += 1
        elif value > 20 and value < 40:
            c += 1
        elif value > 40 and value < 60:
            d += 1
        elif value > 60 and value < 80:
            e += 1
        elif value > 80 and value < 100:
            f += 1
        else:
            g += 1
    plt.bar(range(len([a, b, c, d, e, f, g])), [a, b, c, d, e, f, g])
    plt.title('age distribution')
    plt.xticks(np.arange(7), ['0-5', '5-20', '20-40', '40-60', '60-80', '80-100', '>100'])
    plt.savefig(path + '\\figure\年龄分布.png')
    plt.show()


def zhonglaonian(file_name):
    # 大于60岁的死因code有多少
    age = get_one_column(file_name, 'age')
    code = get_one_column(file_name, 'BSICD10')
    zhong_lao = []
    for index in range(len(age)):
        if age[index] > 60:
            zhong_lao.append(code[index])
    print(zhong_lao)
    print(len(set(zhong_lao)))
    count = 0
    # 看下根本死因涉及到的code有多少
    code_list = []
    for i in code:
        if i != '^':
            count += 1
            code_list.append(i)
    print(len(set(code_list)))


def workplace(file_name):
    work_place = get_one_column(file_name, 'WORKPLACE')
    base_cause = get_one_column(file_name, 'BASECAUSE')

    print(len(set(work_place)))

    file = codecs.open(path + '\\result\\' + file_name + '\工作地点.csv', 'w', encoding='utf-8')
    for index in range(len(work_place)):
        if work_place[index] != '^' and base_cause[index] != '^':
            file.write(work_place[index] + " " + base_cause[index] + '\n')
        if '粉' in work_place[index]:
            print(work_place[index])
    file.close()


def child_cause(file_name):
    child = get_one_column(file_name, 'PERSONAL_TYPE')
    cause = get_one_column(file_name, 'BASECAUSE')
    file = codecs.open(path + '\\result\\' + file_name + '\儿童死因统计.csv', 'w', encoding='utf-8')
    for index in range(len(child)):
        if child[index] == '五岁以下' or child[index] == '5岁以下儿童':
            file.write(child[index] + "," + cause[index] + "\n")
    file.write('\n')


# 得到cdc系统用的icd标准表
def get_standard_ICD(ICD_file):
    col_name = []
    col_name_original= []
    col_ICD = []
    #  读取ICD对应表文件 excel
    # icd_ref_name = 'ICD-10_reference'
    if '类目总表' in ICD_file:
        icd_ref_name = 'ICD-10类目总表'
        XLSX_FIlE = os.getcwd() + "\data\\" + icd_ref_name + ".xlsx"
        SHEET_NAME = 'Sheet1'

        workbook = xlrd.open_workbook(XLSX_FIlE)

        sheet = workbook.sheet_by_name(SHEET_NAME)

        # 抽取第一列和第三列做成dict
        col_ICD = sheet.col_values(0)
        col_name_original = sheet.col_values(1)

    # ********************************************************************************************
    # 读取ICD对应表文件csv icd-10系统对照表
    elif '系统对照表' in ICD_file:
        table = pd.read_csv('D:\stage\data_process_系统对照表\data\icd-10系统对照表_1.csv', encoding='utf-8')
        table = table.fillna(value='^')
        col_ICD = table['CODE'].tolist()
        col_name_original = table['ICDCNNAME'].tolist()
    # # ********************************************************************************************

    for value in col_name_original:
        if value != '^':
            value = value.replace(" *", "").replace("*", "")
            col_name.append(value)
        else:
            col_name.append(value)

    # 构建ICD码和疾病名称的索引表
    dic = {}
    count = 0
    for index in range(len(col_ICD)):
        if col_ICD[index] in dic.keys():
            count += 1
            dic[col_ICD[index]].append(col_name[index])
        else:
            count += 1
            dic[col_ICD[index]] = []
            dic[col_ICD[index]].append(col_name[index])
    print("reference中唯一的code数：", len(dic))  # 9652
    print("reference中ICD对应表的总长度: ", count)  # 21197
    return dic


# 得到CDC数据中的全部cause list和icd list
def get_CDC_ICD(file_name):
    if os.path.exists(path + '\\result\\' + file_name + '\死因_ICD_总表.csv'):
        table = pd.read_csv(path + '\\result\\' + file_name + '\死因_ICD_总表.csv', encoding='utf_8')
    else:
        abcdBase_table(file_name)
        table = pd.read_csv(path + '\\result\\' + file_name + '\死因_ICD_总表.csv', encoding='utf_8')
    # 定义要抽取的列名称
    cause_name = ['A_CAUSE', 'B_CAUSE', 'C_CAUSE', 'D_CAUSE', 'OTHER1_CAUSE', 'BASECAUSE']
    icd_name = ['A_ICD10', 'B_ICD10', 'C_ICD10', 'D_ICD10', 'OTHER1_ICD10', 'BSICD10']
    # 初始化列内容的列表
    cause_list_original = []
    cause_list = []
    icd_list = []
    # 将所有6列的信息全部整合到一起
    for name in cause_name:
        cause_list_original.extend(table[name].tolist())
    for icd in icd_name:
        icd_list.extend(table[icd].tolist())
    for value in cause_list_original:
        value = value.replace('*', '').replace(' *', '').replace(',', '，')
        cause_list.append(value)
    # # 将同一个ICD code对应的诊断描述作为这个code(key)的值,例如: W22.6: ['撞在其他物体上或被其', '撞在其他物体上或被其他物体击中（工业和建筑区域）*']
    # dict = {}
    # non_vide = 0
    # for index in range(len(icd_list)):
    #     if icd_list[index] != '^' and cause_list[index] != '^':
    #         non_vide += 1
    #         if icd_list[index] in dict.keys():
    #             if cause_list[index] not in dict[icd_list[index]]:
    #                 dict[icd_list[index]].append(cause_list[index])
    #         else:
    #             dict[icd_list[index]] = []
    #             dict[icd_list[index]].append(cause_list[index])
    # # 处理CDC的诊断描述.例如 W22.6: ['撞在其他物体上或被其', '撞在其他物体上或被其他物体击中（工业和建筑区域）*'],前者是后者的一个子字符串,则编码W22.6只对应到后一项
    # # 思路:先将code所对应的诊断描述的list按照字符串长度进行排序,在从前往后进行比对,看当前值是否是后面一些值的子字符串.如果是,则把他们存在remove列表里面.之后对dict[key]进行一个循环删除.
    # # 这一步不直接删的原因是,如果删了,下一次在迭代index的时候会出错
    # remove = []
    # for key, value in dict.items():
    #     if len(value) > 1:
    #         value_sorted = sorted(value, key=lambda i:len(i), reverse=False)
    #         for index in range(len(value_sorted)):
    #             lis = value_sorted[index+1:]
    #             for v in lis:
    #                 if value_sorted[index] in v:
    #                     remove.append(value_sorted[index])
    #     for i in remove:
    #         if i in dict[key]:
    #             dict[key].remove(i)
    #     # 这一步中,在每一个dict的key, value项操作之后,要将remove清空,不然他会一直append,造成有些集合删除完之后为空.
    #     remove = []
    # print("CDC中唯一的code数：", len(dict))  # 2534
    # print('CDC中ICD成对出现的数据的条数：', non_vide)  # 284550
    # # print(dict)
    dict = {}
    return cause_list, icd_list, dict


# 统计CDC数据中一个code所对应的诊断名称的个数,生成统计图片,并生成CDC数据中不只有一个诊断名称的编码的统计文件
def CDC_code_text_match(ICD_file, file_name):
    _, _, dic = get_CDC_ICD(file_name)
    dic_len = {}
    file = codecs.open(path + '\\result\\' + file_name + '\不只有一个诊断名称的编码.txt', 'w', encoding='utf-8')
    for key in dic.keys():
        if len(dic[key]) != 1:
            file.write(key + ' ' + str(dic[key]) + '\n')
        if len(dic[key]) in dic_len.keys():
            dic_len[len(dic[key])] += 1
        else:
            dic_len[len(dic[key])] = 1
    file.close()
    # print(dic_len)
    print("CDC的编码结果涉及到的一个编码多个名称的统计：", len(dic_len))

    title = '(纵轴数据)个code有(横轴数据)个诊断描述'
    num_text = []
    total_number = []
    for key, value in dic_len.items():
        num_text.append(key)
        total_number.append(value)
    count_one = frequency_base_code(ICD_file, file_name)
    total_number[0] = total_number[0] - count_one
    data_name = (title)
    table_name = num_text  # table_name
    data_value = total_number  # data_value
    graphic(data_name, table_name, data_value, title, max(data_value)+50)


# TODO: 以code来看，如J18: ['肺炎'; '细菌性肺炎']。只要这个list是标准ICD list的子集，就认为是匹配的上的code
# TODO:下面改了方法，将code和诊断描述拉通看的。不是作为一个列表，求子集。
# 按照code中诊断描述完全匹配的方法来找到CDC和ICD中能匹配的code
def ICD_CDC_text_match(ICD_file, file_name):
    dic_ICD = get_standard_ICD(ICD_file)
    _, _, dic_CDC = get_CDC_ICD(file_name)

    file = codecs.open(path + '\\result\\' + file_name + '\CDC与ICD同样的编码写的不一样的诊断名称的例子.csv', 'w', encoding='utf-8')
    file.write('CDC icd,CDC诊断名称,ICD诊断名称' + '\n')
    file_2 = codecs.open(path + '\\result\\' + file_name + '\ICD中不存在的CDC中的编码.csv', 'w', encoding='utf-8')
    file_2.write('CDC编码,CDC描述' + '\n')
    file_3 = codecs.open(path + '\\result\\' + file_name + '\ICD中不存在的CDC中的c除三位码、XWVY的编码.csv', 'w', encoding='utf-8')
    file_3.write('CDC编码,CDC描述' + '\n')
    file_4 = codecs.open(path + '\\result\\' + file_name + '\CDC与ICD同样的描述写的不一样的编码的例子.csv', 'w', encoding='utf-8')
    file_4.write('CDC编码,CDC描述（描述后面的编码是该描述对应的ICD标准表中对应的编码）,CDC的编码对应的ICD的code' + '\n')
    file_5 = codecs.open(path + '\\result\\' + file_name + '\CDC与ICD同样的描述写的不一样的编码的编码比较.csv', 'w', encoding='utf-8')
    file_5.write('CDC编码,ICD编码' + '\n')

    file_6 = codecs.open(path + '\\编码匹配.csv', 'w', encoding='utf-8')

    file_one = codecs.open(path + '\CDC与ICD同样的编码不一样的诊断名称\\' + file_name + '\CDC编码有一个诊断名称.csv', "w", encoding='utf-8')
    file_two = codecs.open(path + '\CDC与ICD同样的编码不一样的诊断名称\\' + file_name + '\CDC编码有2诊断名称.csv', "w", encoding='utf-8')
    file_three = codecs.open(path + '\CDC与ICD同样的编码不一样的诊断名称\\' + file_name + '\CDC编码有3诊断名称.csv', "w", encoding='utf-8')
    file_other = codecs.open(path + '\CDC与ICD同样的编码不一样的诊断名称\\' + file_name + '\CDC编码有其他个数个诊断名称.csv', "w", encoding='utf-8')

    file_one.write('CDC编码,CDC诊断描述,ICD诊断描述' + '\n')
    file_two.write('CDC编码,CDC诊断描述,ICD诊断描述' + '\n')
    file_three.write('CDC编码,CDC诊断描述,ICD诊断描述' + '\n')
    file_other.write('CDC编码,CDC诊断描述,ICD诊断描述' + '\n')

    CDC_code_length = len(dic_CDC)

    well_match = 0
    not_match = 0
    not_in_ICD = 0
    three_digit = 0
    vwxy_not_in = 0
    vwxy_not_match = 0

    well_match_one = 0
    well_match_two = 0
    well_match_other = 0

    for key in dic_CDC.keys():
        if key in dic_ICD.keys():
            # for value in dic_CDC[key]:
            #     if value in dic_ICD[key]:
            #         well_match += 1
            #     else:
            #         not_match += 1
            # dic_CDC和dic_ICD中的key的list都是没有重复值的，因此只要看dic_CDC中某个key值对应的list
            # 是不是dic_ICD中这个key值对应的list的自己就可以判断dic_CDC中某个诊断编码对应的诊断名称是不是
            # 与ICD reference中的完全匹配
            if set(dic_ICD[key]) >= set(dic_CDC[key]):
                well_match += 1
                if len(dic_CDC[key]) == 1:
                    well_match_one += 1
                    file_6.write(str(dic_CDC[key]) + " " + str(dic_ICD[key]) + "\n")
                elif len(dic_CDC[key]) == 2:
                    well_match_two += 1
                    # print(str(dic_CDC[key]) + " " + str(dic_ICD[key]))
                else:
                    well_match_other += 1
            else:
                not_match += 1
                if key[0] == 'V' or key[0] == 'W' or key[0] == 'X' or key[0] == 'Y':
                    vwxy_not_match += 1
                # 得到某个Key所对应的CDC描述里面对应到ICD的编码
                for value in dic_CDC[key]:
                    for keys in dic_ICD.keys():
                        if value in dic_ICD[keys]:
                            if keys != key:
                                if value in dic_CDC[key]:
                                    dic_CDC[key].remove(value)
                                    dic_CDC[key].append(value + " " + keys)
                file_4.write(key + ',' + str(dic_CDC[key]) + str(dic_ICD[key]) + '\n')
                file_5.write(key + ',' + keys + '\n')
                file.write(key + ',' + str(dic_CDC[key]) + ',' + str(dic_ICD[key]) + '\n')
                # 把CDC诊断名称列表有1 2 3和其他长度的分开
                if len(dic_CDC[key]) == 1:
                    file_one.write(key + ',' + str(dic_CDC[key]) + ',' + str(dic_ICD[key]) + '\n')
                elif len(dic_CDC[key]) == 2:
                    file_two.write(key + ',' + str(dic_CDC[key]) + ',' + str(dic_ICD[key]) + '\n')
                elif len(dic_CDC[key]) == 3:
                    file_three.write(key + ',' + str(dic_CDC[key]) + ',' + str(dic_ICD[key]) + '\n')
                else:
                    file_other.write(key + ',' + str(dic_CDC[key]) + ',' + str(dic_ICD[key]) + '\n')
        else:
            not_in_ICD += 1
            if len(key) == 3:
                three_digit += 1
            # V, W, X, Y涉及到交通事故、家中意外、自杀、杀虫剂等具毒性化学药品、不明原因后遗症等
            # 统计四位的这种码 在ICD10中被分类为附加编码章。（疾病和死亡的外因）
            elif key[0] == 'V' or key[0] == 'W' or key[0] == 'X' or key[0] == 'Y':
                vwxy_not_in += 1
            else:
                file_3.write(key + "," + str(dic_CDC[key]) + '\n')
            file_2.write(key + "," + str(dic_CDC[key]) + '\n')
    file_one.close()
    file_two.close()
    file_three.close()
    file_other.close()
    print("CDC code的个数：", CDC_code_length)
    print('CDC和ICD完全匹配的编码个数：', well_match)
    print("只含有一个诊断描述的编码匹配到的个数：", well_match_one)
    print("有2个诊断描述的编码匹配到的个数：", well_match_two)
    print("含1 2外个诊断描述的编码匹配到的个数：", well_match_other)

    print('CDC和ICD不能完全匹配的编码个数：', not_match)
    print('CDC和ICD不能完全匹配的V W X Y开头的编码个数：', vwxy_not_match)
    print('CDC中不在ICD中的编码个数：', not_in_ICD)
    print('CDC中不在ICD中的三位编码个数：', three_digit)
    print('CDC中不在ICD中的V W X Y开头的编码个数：', vwxy_not_in)


# 根本死因编码频数统计: key是CDC给的编码 + ICD库中的编码名称 或者 CDC库中的编码名称
def frequency_base_code(ICD_file, file_name):
    # 诊断名称对应到ICD
    dict_ICD = get_standard_ICD(ICD_file)
    # 诊断名称对应到CDC
    # dict_ICD = get_CDC_ICD()

    base_icd = get_one_column(file_name, 'BSICD10')
    dic = {}
    for value in base_icd:
        if value in dict_ICD.keys():
            if (value + ' @ ' + str(dict_ICD[value])) in dic.keys():
                dic[value + ' @ ' + str(dict_ICD[value])] += 1
            else:
                dic[value + ' @ ' + str(dict_ICD[value])] = 1
        else:
            if value in dic.keys():
                dic[value] += 1
            else:
                dic[value] = 1
    file_sorted_code = codecs.open(path + '\\result\\' + file_name + '\根本死因编码频数统计_对应到ICD.txt', 'w', encoding='utf-8')
    sort_code = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for value in sort_code:
        file_sorted_code.write(str(value))
        file_sorted_code.write('\n')
    file_sorted_code.close()
    count_one = 0
    for value in dic.values():
        if value == 1:
            count_one += 1
    # 只出现了一次的编码
    return count_one


# 查看调查报告中一共有多少不为空的死亡描述。
# 将不为空的死亡描述对应到某张表中，（通过cardid）
# 将有不为空死亡描述的cardid下的死因链拿出来做成表 “死因链_调查报告”，在result下
def num_report(file_name):
    # 获取表的id
    card_id = get_one_column(file_name, 'CARDID')

    t, _ = get_table_length(file_name)
    total_t = t[['CARDID', 'A_CAUSE', 'A_ICD10', 'B_CAUSE', 'B_ICD10', 'C_CAUSE', 'C_ICD10', 'D_CAUSE', 'D_ICD10',  'OTHER1_CAUSE', 'OTHER1_ICD10', 'BASECAUSE', 'BSICD10']]
    total_t.to_csv(path + '\\result\\' + file_name + '\死因链.csv', index=None)

    # 获取全国死亡表
    table = pd.read_csv(path + '\death17_调查记录_全国.csv', encoding='utf-8')
    # 将死亡表中空值用这个值代替
    table = table.fillna(value='^')
    # 获取全国死亡表中的id
    card_id_global = table["CARDID"].tolist()

    # 获取全国死亡表中的调查内容
    symptom = table["SYMPTOM"].tolist()

    # 将全国死亡表的id和调查内容联系做成一个dict
    dic = {}
    for index in range(len(card_id_global)):
        dic[card_id_global[index]] = symptom[index]
    # CARDID,SYMPTOM,DEATHREASON,AUDIT_NOTE

    # 能对应到的总人数
    match = 0
    # 有调查结果的总人数
    have_symptom = 0
    # 调查结果的长度统计，每一个的长度作为list的元素之一
    len_symptom = []
    #  调查结果存储
    symptom = []

    file_out = codecs.open(path + '\\result\\' + file_name + '\不为空的调查报告.csv', 'w', encoding='utf-8')
    file_out.write('CARDID,report' + '\n')
    for item in card_id:
        if item in dic.keys():
            match += 1
            if dic[item] != '^':
                have_symptom += 1
                len_symptom.append(len(dic[item]))
                symptom.append(dic[item])
                file_out.write(item + ',' + dic[item].replace(',', '，') + '\n')
    df_city = pd.read_csv(path + '\\result\\' + file_name + '\死因链.csv', encoding='utf-8')
    df_global = pd.read_csv(path + '\\result\\' + file_name + '\不为空的调查报告.csv', encoding='utf-8')
    result = pd.merge(df_city, df_global)
    result.to_csv(path + '\\result\\' + file_name + '\死因链_调查报告.csv', index=None)

    # 统计一下全国死亡表中一共有多少个调查报告
    total_non_null = 0
    for value in dic.values():
        if value != '^' and value != '无':
           total_non_null += 1
    print("全国死亡表中一共有多少个调查报告: ", total_non_null)

    print("能与 " + file_name + " 的表匹配到的全国表中id数：", match)
    print("有死亡描述的id匹配数：", have_symptom)
    max_text = max(len_symptom)
    min_text = min(len_symptom)
    avg_text = sum(len_symptom)/have_symptom
    print(max_text, min_text, avg_text)
    # 将各种长度的文本输出考察文本格式
    for item in symptom:
        if len(item) == max_text:
            print("死亡描述长度最长为：", item)
        if len(item) == min_text:
            print("长度最小为：", item)
        if len(item) == 56:
            print("平均长度为：", item)


# 将诊断名称与CDC使用的标准ICD库进行匹配。
# 采用国际类目表、亚目表进行匹配扩充。
# 由于写法造成的没有匹配，采用规则的方法将其纳入正确匹配的列表。如中文逗号、多“的”少“的”等等
# 并返回国际标准的ICD 类目、亚目字典。
def ICD_match(ICD_file, file_name):
    # 获得CDC的cause和icd列表
    cause_list, ICD_list, _ = get_CDC_ICD(file_name)
    # 获得CDC系统用的ICD reference
    dic_icd_cdc = get_standard_ICD(ICD_file)
    print('所有死因链数据汇总：', len(ICD_list))

    # # 获得亚目表 icd reference
    XLSX_FIlE = os.getcwd() + "\data\\4位代码亚目表（ICD-10）.xls"
    SHEET_NAME = '亚目'

    # 获取.xlsx文件的所有sheet列表
    workbook = xlrd.open_workbook(XLSX_FIlE)
    sheet = workbook.sheet_by_name(SHEET_NAME)

    # 抽取第一列和第2列做成dict
    col_ICD = sheet.col_values(1)
    col_name = sheet.col_values(2)

    dic_2011_ICD = {}
    for index in range(len(col_ICD)):
        if col_ICD[index] in dic_2011_ICD.keys():
            dic_2011_ICD[col_ICD[index]].append(col_name[index])
        else:
            dic_2011_ICD[col_ICD[index]] = []
            dic_2011_ICD[col_ICD[index]].append(col_name[index])

        # # 获得类目表 icd reference
    leimu = os.getcwd() + "\data\\3位代码类目表（ICD-10）.xls"
    sheet_name = '类目'

    # 获取.xlsx文件的所有sheet列表
    workbook_leimu = xlrd.open_workbook(leimu)
    sheet_leimu = workbook_leimu.sheet_by_name(sheet_name)

    # 抽取第一列和第三列做成dict
    col_ICD_leimu = sheet_leimu.col_values(0)
    col_name_leimu = sheet_leimu.col_values(1)

    for index in range(len(col_ICD_leimu)):
        if col_ICD_leimu[index] in dic_2011_ICD.keys():
            dic_2011_ICD[col_ICD_leimu[index]].append(col_name_leimu[index])
        else:
            dic_2011_ICD[col_ICD_leimu[index]] = []
            dic_2011_ICD[col_ICD_leimu[index]].append(col_name_leimu[index])
    # 先在CDC中进行匹配再在类目亚目表中进行匹配
    count_cdc_ICD = 0
    # count_2011_ICD = 0
    non_vide = 0
    my_count = 0
    C = 0
    subset = 0
    # 把没有匹配到的cause和list对写入文件
    file = codecs.open(path + '\编码匹配\\' + file_name + '\编码匹配.csv', 'w', encoding='utf-8')
    file.write('数据集中诊断名称,数据集中诊断编码,CDC用的ICD表或者国际类目亚目表中的诊断名称' + '\n')

    # file_diff_code = codecs.open(path + '\编码匹配\\' + file_name + '\编码错误.csv', 'w', encoding='utf-8')
    # file_diff_code.write('数据集中诊断名称,数据集中诊断编码,CDC用的ICD表或者国际类目亚目表中的诊断名称,CDC用的ICD表或者国际类目亚目表中的诊断编码' + '\n')

    not_false = ['肠未特指的疾病','未特指的唐氏综合征', '盲，单眼', '肺栓塞提及急性肺源性', '肺结核，未提及细菌学或组织学的证实','高血压', '未特指的败血症', '脑其他特指的疾患', '前壁急性透壁性心肌梗死', '肾终末期疾病', '脑卒中，未特指为出血或梗死',
                 '小肠克罗恩病', '血容量不足性休克', '主动脉（瓣）关闭不全', '主要由于变应性哮喘','高血压心脏病伴有（充血性）心力',
                 '肾病综合征（未特指）', '扩张型心肌病', '其他肥厚型心肌病', '梗阻性肥厚型心肌病', '神经系统未特指的变性性疾病',
                 '心房过早除极', '食物和呕吐物引起的肺', '食物和呕吐物引起的肺炎', '支气管扩张(症)','心包未特指的疾病',
                 '非风湿性三尖（瓣）关闭不全', '下壁急性透壁性心肌梗死', '肾功能损害引起的痛风', '肺栓塞未提及急性肺源性心脏病',
                 '呼吸道结核和未特指结核的后遗症', '胸主动脉瘤破裂', '腹主动脉瘤破裂', '大脑动脉血栓形成引起的脑梗死','肺结核，经未特指的方法所证实',
                 '未特指的癫\\xB0G', '未特指的下肢静脉炎和血栓性静脉炎','未特指的先天性心脏畸形', '中毒性肝病伴有肝炎，不可归类在他处者', '肺结核，经显微镜下痰检查证实，伴有或不伴有痰培养',
                 '高血心脏和肾脏病伴有（充血性）心力衰竭','脑未特指的先天性畸形', '中度精神发育迟缓（显著的行为缺陷，需要加以关注或治疗）',''
                 '二尖（瓣）关闭不全', '其他特指的肝病', '未特指部位的主动脉瘤破裂', '下肢动脉瘤', '股静脉的静脉炎和血栓性静脉炎',
                 '镇癫\\xB0G药、镇静催眠药、抗帕金森病药和对精神有影响的药物的故意自毒及暴露于该类药,不可归类在他处者（家）',
                 '盲,单眼', '镇癫\\xB0G药、镇静催眠药、抗帕金森病药和对精神有影响的药物的故意自毒及暴露于该类药,不可归类在他处者（未特指场',
                 '心衰', '心衰竭', '急性左心衰', '急性左心衰竭', '其他含硅［矽］粉尘引起的肺尘埃沉着病', '药物性骨质疏松', '轻度精神发育迟缓（未提及行为缺陷）',
                 '髂动脉瘤', '神经系统其他特指的变性性疾病', '未特指的精神发育迟缓', '慢性梗阻性肾盂肾炎', '中枢神经系统其他特指的疾患', '胃动态未定或动态未知的肿瘤',
                 '主要为变应性哮喘', '使用可卡因引起的精神和行为障碍（依赖综合征）', '脑损害和功能障碍及躯体疾病引起的其他特指的精神障碍', '主动脉其他和未特指部位的栓塞和血栓形成',
                 '淋巴、造血和有关组织动态未定或动态未知的肿瘤', '肾病综合征（局灶性和节断性肾小球损害）', '使用酒精引起的精神和行为障碍（未特指的精神和行为障碍）',
                 '慢性肾炎综合征（弥漫性肾小球膜性增生性肾小球肾炎）', '其他的银屑病', '消化系统其他特指的疾病', '心脏未特指的损伤', '克罗伊茨费尔特D雅各布病',
                 '使用大麻类物质引起的精神和行为', '其他梗阻性和反流性尿路病', '颈部和躯干其他特指损伤的后遗症',
                 '轻度精神发育迟缓（未提及行为缺', '使用酒精引起的精神和行为障碍（', '石棉和其他矿物纤维引起的肺尘埃', '其他败血症', '念珠菌性败血症',
                 '颈部开放性伤口累及喉和气管', '其他和未特指的过早除极', '酒精性神经系统变性', '帕金森症', '其他的胆石症', '煤炭工肺尘埃沉着病', '其他特指的败血症',
                 '特指的癫\\xB0G综合征', '其他特指的上呼吸道疾病', '分类于他处的疾病引起的脑其他特', '腰椎骨折', '其他含硅［矽］粉尘引起的肺尘埃', '夸希奥科病[恶性营养不良病]',
                 '一氧化碳中毒', '在颈水平的未特指血管的损伤', '腰椎和骨盆其他和未特指部位的扭', '肺静脉连接完全异常', '巴德－基亚里综合征', '其他癫\\xB0G', '下肢浅表脉管的静脉炎和血栓性静', '其他特指的心律失常',
                 '在膝水平的创伤性切断', '心室过早除极', '脑梗后遗症', '其他舞蹈症', '肾病综合征', '其他和未特指溶血性疾病引起的胎', '胸腹主动脉瘤破裂', '其他器官结核的后遗症', '大脑动脉未特指的闭塞或狭窄引起',
                 '未特指部位的静脉炎和血栓性静脉', '有症状性神经梅毒', '其他革兰氏阴性病原体性败血症', '肾病综合征（其他）', '累及胸部伴有腹部、下背和骨盆的', '其他特指传染病和寄生虫病的后遗',
                 '单克隆丙种球蛋白血症', '风湿性主动脉瓣关闭不全', '其他特指的肺源性心脏病', '未特指部位的急性透壁性心肌梗死', '高血压脑病', '成人肥厚性幽门狭窄', '心脏切开术后综合征',
                 '未特指的链球菌性败血症', '急性胃扩张', '主动脉其他和未特指部位的栓塞和', '使用可卡因引起的精神和行为障碍', '吞咽困难', '胸内器官伴有腹内和盆腔内器官的', '其他和未特指部位的口良性肿瘤',
                 '风湿性二尖瓣关闭不全', '维斯科特D奥尔德里奇综合征', '肠其他和未特指部位的原位癌', '中度精神发育迟缓（未提及行为缺', '交界性过早除极', '使用酒精引起的精神和行为障碍（', '尺骨和桡骨下端均骨折',
                 '肾病综合征（弥漫性膜性肾小球肾', '脑损害和功能障碍及躯体疾病引起','未特指的动态未定或动态未知的肿瘤', '肠、腹膜和肠系膜淋巴结的结核', '肺炎支原体急性支气管炎', '使用大麻类物质引起的精神和行为', '慢性缺血性心脏病(冠心病）',
                 '极重度精神发育迟缓（未提及行为', '三尖瓣关闭不全', '选择性维生素Ｂ12吸收不良伴有蛋', '累及上肢伴有下肢多个部位的骨折', '马方综合征', '高血压心脏病', '在腕和手水平的未特指血管的损伤',
                 '未特指的分枝杆菌感染', '泌尿生殖系结核的后遗症', '其他和未特指的右束支传导阻滞', '先天性主动脉瓣关闭不全', '未特指的肺尘埃沉着病', '在髋和大腿水平的多血管损伤', '未特指的腹疝',
                 '银屑病[牛皮癣]', '非溶血性疾病引起的胎儿水肿', '脑损害和功能障碍及躯体疾病引起', '在髋和大腿水平的未特指血管的损', '累及胸部伴有下背和骨盆的骨折', '颈动脉瘤', '颅骨穹窿骨折',
                 '伴有免疫球蛋白Ｍ［IgM］增多的', '高血压心脏病伴有（充血性）心力衰竭', '脑卒中后遗症，未特指为出血或梗死', '皮肤和皮下组织未特指的局部感染',
                 '颈部和躯干未特指损伤的后遗症', '寻常型天疱疮', '肾病综合征（局灶性和节断性肾小', '前壁急性透壁性心肌梗', '其他梗阻性和反流性尿', '肾和输尿管其他特指的', '其他和未特指的过早除',
                 '其他的非风湿性二尖瓣','慢性阻塞性肺病伴有急性下呼吸道','腹主动脉瘤，未提及破裂','肺栓塞提及急性肺源性心脏病','胆道未特指的疾病',
                 '下壁急性透壁性心肌梗', '骨和关节结核的后遗症','胰腺内分泌的良性肿瘤', '脑损害和功能障碍及躯', '呼吸道结核和未特指结', '其他含硅［矽］粉尘引', '辐射引起的急性肺部临', '尺骨和桡骨骨干均骨折',
                 '胃和十二指肠其他特指', '口腔粘膜其他和未特指', '消化系统其他特指的疾', '其他固体和液体引起的', '轻度精神发育迟缓（其', '药物和药剂引起的局部', '重度精神发育迟缓（未',
                 '主动脉其他和未特指部', '癫\\xB0B[癫痫]', '大脑动脉栓塞引起的脑', '血液和造血器官其他特', '其他的脊椎关节强硬伴', '累及胸部伴有腹部、下', '颈部和躯干其他特指损',
                 '胰腺内分泌其他特指的', '高血压心脏病不伴有（充血性）心', '未特指的心律失常', '消化系统未特指的疾病', '其他特指的腹疝，不伴有梗阻或坏', '高血压心脏和肾脏病同时伴有（充',
                 '心壁破裂不伴有心包积血作为急性', '脑卒中后遗症，未特指为出血或梗', '主动脉（瓣）狭窄伴有关闭不全', '血液和造血器官未特指的疾病',
                 '未特指的下肢静脉炎和血栓性静脉', '未特指的动态未定或动态未知的肿','股骨部位未特指的骨折','未特指部位的主动脉瘤，未提及破',
                 '石棉和其他矿物纤维引', '其他镇癫\\xB0G药和镇', '中度精神发育迟缓（其', '泌尿生殖系结核的后遗', '其他特指的肺源性心脏', '动脉和小动脉其他特指', '大脑动脉血栓形成引起', '肾病综合征（局灶性和',
                 '未特指部位的主动脉瘤', '极重度精神发育迟缓（', '未特指的沙门菌感染', '累及头部伴有颈部的挤', '皮疹和其他非特异性斑', '晚发性阿尔茨海默病性', '非风湿性三尖（瓣）关', '肺炎杆菌性肺炎',
                 '其他特指的上呼吸道疾', '脑损害和功能障碍及躯', '胆石症', '高血压肾脏病', '泌尿系统其他特指的疾', '轻度精神发育迟缓（未', '其他特指的锥体束外和', '其他特指的颌的疾病', '神经系统其他特指的变',
                 '全身脓疱性银屑病', '石棉和其他矿物纤维引起的肺尘埃沉着病', '中度精神发育迟缓（未提及行为缺陷）', '使用酒精引起的精神和行为障碍（残留性和迟发性精神病性障碍）',
                 '肾病综合征（弥漫性膜性肾小球肾炎）', '未特指的肾炎综合征（弥漫性肾小球膜性增生性肾小球肾炎）', '人类免疫缺陷病毒［HIV］病造成的分枝杆菌感染', '伴有免疫球蛋白Ｍ［IgM］增多的免疫缺陷',
                 '极重度精神发育迟缓（未提及行为缺陷）', '未特指的肺源性心脏病', '高血压心脏病不伴有（充血性）心力衰竭', '高血压肾脏病伴有肾衰竭','未特指的痔不伴有并发','使用酒精引起的精神和','主动脉瓣和二尖瓣未特','其他特指的腹疝，不伴有梗阻或坏疽',
                 '未特指的脑脊膜良性肿','循环系统未特指的操作后疾患','未特指的唐氏综合征[先天愚型]','新生儿未特指的呼吸窘迫', '脑动脉瘤，未破裂',
                 '胰岛素依赖型糖尿病，伴有昏迷', '前臂部位未特指的骨折', '未特指的糖尿病，不伴有并发症', '未特指的侧腭裂伴有单侧唇裂', '未特指的肺源性心',
                 '大脑半球未特指的脑内出血', '腹部动脉瘤破裂', '肺结核，经显微镜下痰检查证实，', '肺结核，细菌学和组织学检查为阴', '未特指的克罗恩病',
                 '未特指的精神发育迟缓（无，或轻', '胸主动脉瘤，未提及破裂', '未特指的睡眠障碍', '新生儿未特指的细菌性脓毒症', '二尖瓣狭窄伴有关闭不全',
                 '急性下壁心肌梗死','未特指的肥胖症', '泌尿系统未特指的疾患', '遗传性肾病，不可归类在他处者（', '高血压心脏病伴心力衰竭', '未特指的梗阻性和反流性尿路病',
                 '子宫未特指的炎性疾病', '未特指的病毒性肝炎，伴有肝昏迷','小腿部位未特指的开放性伤口', '其他的脊椎关节强硬伴有神经根病','头部部位未特指的浅表损伤', '骨密度和结构未特指的疾患',
                 '胸部部位未特指的开放性伤口','高尿酸血症不伴有感染性关节炎体', '使用酒精引起的精神和行为障碍', '其他特指的腹，伴有梗阻，不伴有', '其他的骨质疏松伴有病理性骨折',
                 '新生儿未特指的大脑障碍', '小腿未特指的浅表损伤','中度精神发育迟缓（显著的行为缺', '未特指的病毒性肝炎，不伴有肝昏', '特发于围生期未特指的感染',
                 '颅和面骨未特指的先天性畸形', '其他特指的糖尿病，不伴有并发症', '未特指的胸廓先天性畸形', '骨未特指的连续性疾患', '未特指的血清反应阳性的类风湿性',
                 '未特指的异常的子宫和阴道出血', '肾上腺未特指的疾患', '肛门和直肠未特指的疾病', '腹膜未特指的疾患','大脑动脉夹层形成，未破裂', '高血压心脏病伴有（充',
                 '脑卒中后遗症，未特指', '高血压心脏和肾脏病伴', '高血压肾脏病伴有肾衰', '慢性阻塞性肺病伴有急', '高血压心脏病不伴有（', '未特指的骨质疏松伴有',
                 '神经系统未特指的变性', '高血压心脏和肾脏病同', '胆囊结石伴有其他胆囊', '胆囊结石伴有急性胆囊', '新生儿未特指的呼吸窘', '肺结核，未提及细菌学',
                 '未特指的先天性心脏畸', '传染病或寄生虫病的后', '未特指的腹疝，不伴有', '胃和十二指肠未特指的', '中毒性肝病伴有肝纤维', '甲状腺毒症伴有弥漫性',
                 '脑卒中，未特指为出血', '其他特指的腹疝，伴有','腹主动脉瘤，未提及破', '高血压肾脏病不伴有肾', '消化系统未特指的先天', '未特指的呼吸道结核，', '高血心脏和肾脏病伴有',
                 '糖尿病，伴有肾的并发', '肺栓塞未提及急性肺源', '结缔组织未特指的系统', '未特指的糖尿病，不伴', '其他病原体未特指的肺', '胆管结石不伴有胆管炎',
                 '皮肤和皮下组织未特指', '其他间质性肺病伴有纤', '其他特指的腹，伴有梗阻，不伴有坏疽', '消化系统未特指的先天性畸形', '未特指的血清反应阳性的类风湿性关节炎',
                 '使用其他兴奋剂[包括咖啡因]引起的精神和行为障碍（戒断状态）', '未特指的呼吸道结核，未提及细菌学或组织学的证实', '未特指的腹疝，伴有梗阻，不伴有坏疽', '胰岛素依赖型糖尿病，伴有周围循环并发症', '未特指的精神发育迟缓（无，或轻微的行为缺陷）',
                 '未特指的异常的子宫和', '其他和未特指的分支传', '食管闭锁伴有气管食管', '胸部部位未特指的开放', '中毒性肝病伴有慢性小', '前庭未特指的功能疾患',
                 '肩胛带部位未特指的骨', '慢性肺源性心脏病', '大脑动脉夹层形成，未', '循环系统未特指的操作', '头部部位未特指的浅表','未特指部位的主动脉瘤，未提及破裂',
                 '胎儿和新生儿未特指的颅内(非创伤性)出血', '未特指的病毒性肝炎，不伴有肝昏迷', '未特指的癫\\xB0G大发作（伴有或不伴有小发作）','肺结核，细菌学和组织学检查为阴性',
                 '未特指的癫\\xB0G小发作，不伴有大发作', '中枢神经系统未特指的', '未特指的唐氏综合征',
                 '选择性维生素Ｂ12吸收不良伴有蛋白尿引起的维生素Ｂ12缺乏性贫血', '未特指的高血压心脏和肾脏病', '其他的肠血管疾患','未特指的慢性阻塞性肺病伴有急性',
                 '肺结核，仅经痰培养所证实', '未特指的脑脊膜良性肿瘤', '脑未特指的动态未定或动态未知的', '前臂部位未特指的开放性伤口', '未特指银屑病', '肺结核，经组织学所证实', '高血心脏和肾脏病伴有（充血性）', '未特指的腹疝，不伴有梗阻或坏疽',
                 '颈部部位未特指的开放性伤口', '颈部部位未特指的骨折', '', '其他病原体未特指的肺炎', '头部部位未特指的挤压伤','肺结核，未提及细菌学或组织学的', '中枢神经系统未特指的疾患',
                 '头部部位未特指的开放性伤口', '结缔组织未特指的系统性受累', '食管未特指的疾病', '膀胱未特指的疾患', '上消化道未特指的先天性畸形', '胃和十二指肠未特指的疾病', '腹部、下背和骨盆部位未特指的浅','中毒性肝病伴有肝纤维化和肝硬变', '']
    not_account = ['V', 'W', 'X', 'Y', 'T']

    for index in range(len(ICD_list)):
        if ICD_list[index] != '^' and cause_list[index] != '^':
            non_vide += 1
            if ICD_list[index] in dic_icd_cdc.keys():
                if cause_list[index] in dic_icd_cdc[ICD_list[index]]:
                    count_cdc_ICD += 1
                else:
                    if ICD_list[index][0] == 'C' or ICD_list[index][0] == 'D':
                        C += 1
                    # elif cause_list[index] in not_false:
                    #     subset += 1
                    elif ICD_list[index][0] in not_account:
                        count_cdc_ICD += 1
                    elif dic_icd_cdc[ICD_list[index]][0][0:2] == cause_list[index][0:2] and cause_list[index] in dic_icd_cdc[ICD_list[index]][0]:
                        subset += 1
                    elif cause_list[index][0:2] == dic_icd_cdc[ICD_list[index]][0][0:2] and dic_icd_cdc[ICD_list[index]][0] in cause_list[index]:
                        subset += 1
                    elif cause_list[index].replace('的', '') == dic_icd_cdc[ICD_list[index]][0]:
                        subset += 1
                    elif dic_icd_cdc[ICD_list[index]][0].replace('由于', '') == cause_list[index]:
                        count_cdc_ICD += 1
                    elif cause_list[index].replace('性', '') == dic_icd_cdc[ICD_list[index]][0]:
                        count_cdc_ICD += 1
                    elif cause_list[index].replace('的', '') == dic_icd_cdc[ICD_list[index]][0].replace('的', ''):
                        count_cdc_ICD += 1
                        # TODO 上海的没有用这个条件
                    # elif similarity(cause_list[index], dic_icd_cdc[ICD_list[index]][0]) > 0.9 and (
                    #             '结核' not in cause_list[index]):
                    #     count_cdc_ICD += 1
                    elif '，' in dic_icd_cdc[ICD_list[index]][0]:
                        if cause_list[index].replace('的', '') in dic_icd_cdc[ICD_list[index]][0].split('，')[1] + dic_icd_cdc[ICD_list[index]][0].split('，')[0]:
                            subset += 1
                        elif cause_list[index] in dic_icd_cdc[ICD_list[index]][0].split('，')[1] + dic_icd_cdc[ICD_list[index]][0].split('，')[0]:
                            subset += 1
                        elif cause_list[index] == dic_icd_cdc[ICD_list[index]][0].replace('，', ''):
                            subset += 1
                        elif cause_list[index] == dic_icd_cdc[ICD_list[index]][0].replace('，', '').replace('性', ''):
                            subset += 1
                        else:
                            my_count += 1
                            file.write(cause_list[index] + ',' + ICD_list[index] + ',' + str(dic_icd_cdc[ICD_list[index]]) + '\n')
                    elif ICD_list[index] in dic_2011_ICD.keys():
                        if cause_list[index] in dic_2011_ICD[ICD_list[index]]:
                            count_cdc_ICD += 1
                        else:
                            my_count += 1
                            file.write(cause_list[index] + ',' + ICD_list[index] + ',' + str(dic_icd_cdc[ICD_list[index]]) + '\n')
                            # file.write(cause_list[index] + ',' + ICD_list[index] + ',,' + '\n')
                    else:
                        my_count += 1
                        file.write(cause_list[index] + ',' + ICD_list[index] + ',' + str(dic_icd_cdc[ICD_list[index]]) + '\n')
            elif ICD_list[index] in dic_2011_ICD.keys():
                if cause_list[index] in dic_2011_ICD[ICD_list[index]]:
                    count_cdc_ICD += 1
                else:
                    my_count += 1
                    file.write(cause_list[index] + ',' + ICD_list[index] + ',,' + '\n')
            else:
                my_count += 1
                file.write(cause_list[index] + ',' + ICD_list[index] + ',,' + '\n')
    print('没有找到的icd:', my_count)
    print('CDC中cause和icd数据对都不为空的总数:', non_vide)
    print("count_cdc_ICD: ", count_cdc_ICD + C + subset)
    print('匹配比例：', round((count_cdc_ICD + C + subset)/non_vide, 3))
    file.close()
    return dic_2011_ICD

    # 贵州新疆
    # 用ICD10类目总表
    # 没有找到的icd: 321564
    # CDC中cause和icd数据对都不为空的总数: 439343
    # count_cdc_ICD:  117779
    # 匹配总数： 0.268

    # 贵州新疆
    # 只用ICD10系统对照表
    # 没有找到的icd: 231008
    # CDC中cause和icd数据对都不为空的总数: 439343
    # count_cdc_ICD:  208335
    # 匹配总数： 0.474

    # 上海
    # 只用ICD10系统对照表
    # 没有找到的icd: 179338
    # CDC中cause和icd数据对都不为空的总数: 284550
    # count_cdc_ICD: 105212
    # 匹配总数： 0.37

    # 上海
    # 用ICD10类目总表
    # 没有找到的icd: 39124
    # CDC中cause和icd数据对都不为空的总数: 284550
    # count_cdc_ICD:  245426
    # 匹配总数： 0.863


# 查看生成的编码匹配文件中有多少的诊断名称还在标准诊断名称中
def aide(ICD_file, file_name):
    dic_inte_ICD = ICD_match(ICD_file, file_name)
    table = pd.read_csv(path + '\编码匹配\\' + file_name + '\编码匹配.csv', encoding='utf-8')

    cause = table['数据集中诊断名称'].tolist()
    ICD = table['数据集中诊断编码'].tolist()

    count = 0
    for index in range(len(cause)):
        if cause[index] in list(dic_inte_ICD.values()):
            if list(dic_inte_ICD.keys())[list(dic_inte_ICD.values()).index(cause[index].replace('，', ','))] != ICD[index]:
                print(cause[index], ICD[index], list(dic_inte_ICD.keys())[list(dic_inte_ICD.values()).index(cause[index])])
        else:
            count += 1
    print('不在标准名称中：', count)


# 考察A B C D的多种组合。因为组合关系不只有A_cause;A_cause, A_code; A_cause, A_code, B_cause; ......
def cause_icd_group(file_name):
    dic = {}
    not_blanc_list = []

    # 考虑other
    # a_c, a, b_c, b, c_c, c, d_c, d, other_c, other, base_c, base = base_abcd_match(file_name)
    # data_list = [a_c, a, b_c, b, c_c, c, d_c, d, other_c, other, base_c, base]
    # list_name = ['a_c', 'a', 'b_c', 'b', 'c_c', 'c', 'd_c', 'd', 'other_c', 'other', 'base_c', 'base']

    # 考察A B C D的多种组合
    a_c, a, b_c, b, c_c, c, d_c, d, other_c, other, _, _ = base_abcd_match(file_name)
    print(len(a_c))
    data_list = [a_c, a, b_c, b, c_c, c, d_c, d]
    list_name = ['a_c', 'a', 'b_c', 'b', 'c_c', 'c', 'd_c', 'd']
    for index in range(len(a_c)):
        for i in range(len(data_list)):
            if data_list[i][index] != '^':
                not_blanc_list.append(list_name[i])
        if str(not_blanc_list) in dic.keys():
            dic[str(not_blanc_list)] += 1
        else:
            dic[str(not_blanc_list)] = 1
        not_blanc_list = []

    file_out = codecs.open(path + '\\result\\' + file_name + '\A B C D的cause及ICD的组合.txt', 'w', encoding='utf-8')
    sum = 0
    for key, value in dic.items():
        file_out.write(key + ' ' + str(value) + '\n')
        sum += value
    print(sum)
# cause_icd_group('guizhou_xinjiang')


# 统计仅有A cause的数据有多少，有A cause, A icd的数据有多少条，有完整的A和仅有Bcause ....有完整的A B C D数据的有多少条
# 在有了B的信息之后，A_CAUSE, A_ICD肯定是存在了的

# 更改：这个函数最终用来统计有完整的ABCD的情况下，只有other_code, 只有other_cause, 有other_cause和other_code。code和cause都没有的数量
def death_reason_report(file_name):
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0

    # 统计有多少数据只有other_cause
    count_other_c = 0
    # 统计有多少数据只有other_code
    count_other_code = 0
    # 统计只有other_cause和other_code
    count_other = 0

    # 统计有完整的ABCD和other_code
    ABCD_other_code = 0
    # 统计有完整的ABCD和other_cause
    ABCD_other_c = 0
    # 统计有完整的ABCD和other_cause和other_code
    ABCD_other = 0
    # 统计有完整的ABCD和没有other
    ABCD_no_other = 0

    # 统计有完整的ABCD
    ABCD_total = 0

    a_c, a, b_c, b, c_c, c, d_c, d, other_c, other, base_c, base = base_abcd_match(file_name)
    for index in range(len(a_c)):
        # if a_c[index] != '^' and a[index] == b_c[index] == b[index] == c_c[index] == c[index] == d_c[index] == d[index] == '^':
        #     one += 1
        #     print(a_c[index], base_c[index], base[index])
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] == b[index] == c_c[index] == c[index] == d_c[index] == d[index] == '^':
        #     two += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] == c_c[index] == c[index] == d_c[index] == d[index] == '^':
        #     three += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] == c[index] == d_c[index] == d[index] == '^':
        #     four += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] == d_c[index] == d[index] == '^':
        #     five += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d[index] == d_c[index] == '^':
        #     six += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] == '^':
        #     seven += 1
        # elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^':
        #     eight += 1
        if a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^' and other[index] != '^' and other_c[index] == '^':
            ABCD_other_code += 1
        elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^' and other_c[index] != '^' and other[index] == '^':
            ABCD_other_c += 1
        elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^' and other_c[index] != '^' and other[index] != '^':
            ABCD_other += 1
        elif a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^' and other_c[index] == '^' and other[index] == '^':
            ABCD_no_other += 1

        if a_c[index] != '^' and a[index] != '^' and b_c[index] != '^' and b[index] != '^' and c_c[index] != '^' and c[index] != '^' and d_c[index] != '^' and d[index] != '^':
            ABCD_total += 1

        if a_c[index] == a[index] == b_c[index] == b[index] == c_c[index] == c[index] == d_c[index] == d[index] == other[index] == '^' and other_c[index] != '^':
            count_other_c += 1
        elif a_c[index] == a[index] == b_c[index] == b[index] == c_c[index] == c[index] == d_c[index] == d[index] == other_c[index] == '^' and other[index] != '^':
            count_other_code += 1
        elif a_c[index] == a[index] == b_c[index] == b[index] == c_c[index] == c[index] == d_c[index] == d[index] == '^' and other[index] != '^' and other_c[index] != '^':
            count_other += 1

    # print("只有A_cause, 有A_cause和A_code, 有A_cause, A_code, B_cause......", one, two, three, four, five, six, seven, eight)
    print("有完整的ABCD和other中的一个code:", ABCD_other_code)
    print("有完整的ABCD和other中的一个cause:", ABCD_other_c)
    print("有完整的ABCD和完整的other:", ABCD_other)
    print("有完整的ABCD和没有other:", ABCD_no_other)
    print("有完整的ABCD:", ABCD_total)

    print("只有other_cause, 只有other_code, 有other_cause和other_code: ", count_other_c, count_other_code, count_other)
# death_reason_report('beijing_zhejiang')


if __name__ == "__main__":

    ICD_file = '系统对照表'
    file_name_list = ['guizhou_xinjiang', 'beijing_zhejiang', 'shanghai']

    # 生成'编码匹配.csv文件'
    # get_file(file_name_list[0])
    # describe(file_name_list[2])
    # frequency_base_code(ICD_file, file_name_list[0])
    # ICD_match(ICD_file, file_name_list[0])

    # 死亡报告
    # num_report(file_name_list[0])

    # 查看有多少还在其他标准中
    # aide(ICD_file, file_name_list[0])

    # 生成文件"使用nlp算法生成编码.csv",并且分析错误的位数
    # nlp_code(file_name_list[0])
    # analysis_nlp(file_name_list[0])

    # 用顾根的新算法生成诊断名称对应的标准诊断名称
    # new_nlp_code("guizhou_xinjiang")
# 全国死亡表中一共有多少个调查报告:  2293801
# 能与上海的表匹配到的全国表中id数： 152301
# 有死亡描述的id匹配数： 68826
# 216 1 56.83279574579374