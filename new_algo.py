import codecs
import os
import pandas as pd
import requests
import time
from read_file import abcdBase_table, get_CDC_ICD, get_standard_ICD
import random

path = os.getcwd()


# 请求顾根的新NLP算法API，传入参数诊断名称，得到诊断名称的id。这个过程中出现的ConnectionError. max retries exceed with url '...'.
# [Errno 110041] getaddrinfo failed'...网上找了很多教程，比如在头部加上断开连接的标记，或者增大重试次数都不好使。所以，重新试一次就好了
# ，检查到错误就睡两秒重发。这一步得到的是诊断名称对应的synyi_id
def post_new(cause):
    # 访问链接
    target_url = 'http://medical-ai-nlp-map-concept-2.sy/api/map_concept'
    content = {"func_name": "get_concept_id",
               "arg": {
                   "domain": "disease",
                   "text": cause
               }}
    flag = False
    while not flag:
        try:
            result = requests.post(target_url, json=content)
        except:
            print(u'[%s] HTTP请求失败！！！正在准备重发。。。')
            time.sleep(2)
            continue
        flag = True
    res = result.text

    # if res == '[]':
    #     content = {"func_name": "get_concept_id",
    #                "arg": {
    #                    "domain": "icd10disease",
    #                    "text": cause
    #                }}
    #
    #     flag = False
    #     while not flag:
    #         try:
    #             result = requests.post(target_url, json=content)
    #         except:
    #             print(u'[%s] HTTP请求失败！！！正在准备重发。。。')
    #             time.sleep(2)
    #             continue
    #         flag = True
    #     requests.session().close()
    #     res = result.text
    return res


# 在上一步得到诊断名称的id之后，调用新接口explain，得到这个id对应的标准名称
def post_name(id):
    # 访问链接
    target_url = 'http://medical-ai-nlp-map-concept-2.sy/api/explain'
    content = id

    flag = False
    while not flag:
        try:
            result = requests.post(target_url, content)
        except:
            print(u'[%s] HTTP请求失败！！！正在准备重发。。。')
            time.sleep(2)
            continue
        flag = True
    requests.session().close()

    res = []
    if '}' in result.text:
        # print(result.text)
        tmp = result.text.split('},')
        for item in tmp:
            res.append(item.split(',')[1].split(': ')[1])
    if res:
        return res
    else:
        return result.text


# 只分析每个数据集中最后剩下的不确定的诊断名称-诊断编码对。生成"使用新的nlp算法生成标准诊断名称.csv"。最后我们有的是这个诊断名称对应的标准诊断名称。
# *************************后面暂时还没有用************************************
def new_nlp_code(file_name):
    file_in = pd.read_csv(path + '\编码匹配\\' + file_name + '\编码匹配.csv', encoding='utf-8')
    cause = file_in['数据集中诊断名称'].tolist()
    icd = file_in['数据集中诊断编码'].tolist()

    # cause_original, icd_original, _ = get_CDC_ICD(file_name)
    # icd = []
    # cause = []
    # for index in range(len(cause_original)):
    #     if cause_original[index] != '^' and icd_original[index] != '^':
    #         if cause_icd_group([index]) not in cause:
    #             cause.append(cause_original[index])
    #         if icd_original[index] not in icd:
    #             icd.append(icd_original[index])
    # num_code = len(cause)

    file = codecs.open(path + '\新NLP算法\\' + file_name + '\\nlp\使用新的nlp算法生成标准诊断名称.csv', 'w', encoding='utf-8')
    file.write('诊断名称,诊断编码,算法生成的标准名称' + '\n')
    for index in range(len(cause)):
        standard_name = post_name(post_new(cause[index]))
        file.write(cause[index] + ',' + icd[index] + ',' + standard_name + '\n')


# 分析表中有多少条text_code数据，以及去重和不去重的数据总数。并生成去重和不去重的名称，code表
def statistic_text_code(file_name):
    abcdBase_table(file_name)
    cause_original, icd_original, _ = get_CDC_ICD(file_name)
    print(len(cause_original))
    print(len(icd_original))
    total_lines = round(len(icd_original)/6, 0)
    print("地区数据总条数：", total_lines)
    len_text_code = 0
    len_text_or_code = 0
    text_code_deduplicate = set()

    file = codecs.open(path + '\内部质量同步表\\' + file_name + '\不去重text_code.csv', 'w', encoding='utf-8')
    file_deduplicate = codecs.open(path + '\内部质量同步表\\' + file_name + '\去重text_code.csv', 'w', encoding='utf-8')
    file.write('CDC诊断名称,CDC诊断编码' + '\n')
    file_deduplicate.write('CDC诊断名称,CDC诊断编码' + '\n')

    only_cause = set()
    only_icd = set()
    cause = []
    icd = []

    for index in range(len(cause_original)):
        if cause_original[index] != '^' and icd_original[index] != '^':
            len_text_code += 1
            text_code_deduplicate.add(cause_original[index] + '@' + icd_original[index])
            cause.append(cause_original[index])
            icd.append(icd_original[index])
            file.write(cause_original[index] + ',' + str(icd_original[index]) + '\n')
        elif cause_original[index] != '^' and icd_original[index] == '^':
            len_text_or_code += 1
            only_cause.add(cause_original[index])
        elif cause_original[index] == '^' and icd_original[index] != '^':
            len_text_or_code += 1
            only_icd.add(icd_original[index])

    for item in text_code_deduplicate:
        file_deduplicate.write(item.split('@')[0] + ',' + str(item.split('@')[1]) + '\n')

    table = pd.read_csv(path + '\内部质量同步表\\' + file_name + '\去重text_code.csv', encoding='utf-8')
    cause_deduplicate = table['CDC诊断名称'].tolist()
    icd_deduplicate = table['CDC诊断编码'].tolist()

    not_conclude_code = 0
    not_conclude_cause = 0
    file_not_conclude_code = codecs.open(path + '\内部质量同步表\\' + file_name + '\只有code的数据没有包含在去重数据中的数量.csv', 'w', encoding='utf-8')
    file_not_conclude_cause = codecs.open(path + '\内部质量同步表\\' + file_name + '\只有cause的数据没有包含在去重数据中的数量.csv', 'w', encoding='utf-8')
    file_not_conclude_code.write('诊断编码' + '\n')
    file_not_conclude_cause.write('诊断名称' + '\n')
    for item in only_icd:
        if item not in icd_deduplicate:
            not_conclude_code += 1
            file_not_conclude_code.write(item + '\n')
    for i in only_cause:
        if i not in cause_deduplicate:
            not_conclude_cause += 1
            file_not_conclude_cause.write(i + '\n')

    # dict_cause = {}
    # for v in cause:
    #     if v in dict_cause.keys():
    #         dict_cause[v] += 1
    #     else:
    #         dict_cause[v] = 1
    # not_conclude_cause_duplicate = 0
    # file_not_conclude_cause_dup = codecs.open(path + '\内部质量同步表\\' + file_name + '\只有cause的数据没有包含在不去重数据中的数量.csv', 'w', encoding='utf-8')
    # for v_only_cause in only_cause:
    #     if v_only_cause not in dict_cause.keys():
    #         print(1111)
    #         print(dict_cause[v_only_cause])
    #         not_conclude_cause_duplicate += dict_cause[v_only_cause]
    #         file_not_conclude_cause_dup.write(v_only_cause + '\n')
    #
    # dict_code = {}
    # for v in icd:
    #     if v in dict_code.keys():
    #         dict_code[v] += 1
    #     else:
    #         dict_code[v] = 1
    # not_conclude_code_duplicate = 0
    # file_not_conclude_code_dup = codecs.open(path + '\内部质量同步表\\' + file_name + '\只有code的数据没有包含在不去重数据中的数量.csv', 'w', encoding='utf-8')
    # for v_only_code in only_icd:
    #     if v_only_code not in dict_code.keys():
    #         not_conclude_code_duplicate += dict_code[v_only_code]
    #         file_not_conclude_code_dup.write(v_only_code + '\n')

    print('文本_code条数：', len_text_code)
    print('二者之一为空的条数：', len_text_or_code)
    print('去重code_list的条数：', len(text_code_deduplicate))
    print('重复数据条数：', len_text_code - len(text_code_deduplicate))
    print('只有cause，去重数量', len(only_cause))
    print('只有code，去重数量', len(only_icd))
    print('只有cause的条目，cause没有考虑到去重数据集中的数目：', not_conclude_cause)
    print('只有code的条目，code没有考虑到去重数据集中的数目：', not_conclude_code)
    # print('只有cause的条目，cause没有考虑到不去重数据集中的数目：', not_conclude_cause_duplicate)
    # print('只有code的条目，code没有考虑到不去重数据集中的数目：', not_conclude_code_duplicate)

    file.close()
    file_deduplicate.close()
    # 前面5个返回值对应到表格里面的前5行。第六、七、八个对应到11、12、13行C列。
    return total_lines, len_text_code, len_text_or_code, len_text_code - len(text_code_deduplicate), len(text_code_deduplicate), \
           len(only_cause), len(only_icd), not_conclude_cause, not_conclude_code
# statistic_text_code('guizhou')


def synyi_id(file_name, code_file):
    # cause_original, icd_original, _ = get_CDC_ICD(file_name)
    # icd = []
    # cause = []
    # for index in range(len(cause_original)):
    #     if cause_original[index] != '^' and icd_original[index] != '^':
    #         # 按照诊断名称去重的
    #         if cause_original[index] not in cause:
    #             cause.append(cause_original[index])
    #             icd.append(icd_original[index])
    # print(len(cause), len(icd))

    table = pd.read_csv(path + '\内部质量同步表\\' + file_name + '\\' + code_file + '.csv', encoding='utf-8')
    cause = table['CDC诊断名称'].tolist()
    icd = table['CDC诊断编码'].tolist()

    dic = get_standard_ICD("系统对照表")

    file = codecs.open(path + '\内部质量同步表\\' + file_name + '\\synyi_code匹配' + code_file + '.csv', 'w', encoding='utf-8')
    file.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')

    for index in range(len(cause)):
        cdc_synyi = post_new(cause[index])
        if icd[index].upper() in dic.keys():
            for i in dic[icd[index].upper()]:
                standard_synyi = post_new(i)
        else:
            standard_synyi = '[]'
        file.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi + ',' + standard_synyi + '\n')


def synyi_id_analysis(file_name, code_file):
    if code_file == '去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code匹配去重text_code.csv', 'r', encoding='utf-8')
    elif code_file == '不去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code匹配不去重text_code.csv', 'r', encoding='utf-8')
    elif code_file == '去重TrueFalse':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\去重synyi_icd表中code和诊断描述匹配对的实例.csv', 'r', encoding='utf-8')
    elif code_file == '不去重TrueFalse':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\不去重synyi_icd表中code和诊断描述匹配对的实例.csv', 'r', encoding='utf-8')

    cdc_synyi = []
    standard_synyi = []
    cause = []
    icd = []
    for line in file:
        line = line.strip()
        if '[' in line.split(',')[0]:
            line = line.replace('[', '(', 1)
            line = line.replace(']', ')', 1)
        if '[' in line:
            cause.append(line.split(',')[0])
            icd.append(line.split(',')[1])
            cdc_synyi.append('[' + line.split('[')[1].replace('],', ']'))
            standard_synyi.append('[' + line.split('[')[2])

    length_total = len(cdc_synyi)
    same = 0
    not_blank = 0
    both_vide = 0
    vide_cdc = 0
    vide_standard = 0

    file_consis = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\都不为空且一致的例子.csv', 'w', encoding='utf-8')
    file_consis.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')
    file_not_consis = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\都不为空但是不一样的例子.csv', 'w', encoding='utf-8')
    file_not_consis.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')
    file_vide_cdc = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\由诊断文本得到的synyi_id为空的例子.csv', 'w', encoding='utf-8')
    file_vide_cdc.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')
    file_vide_standard = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\由code得到的synyi_id为空的例子.csv', 'w', encoding='utf-8')
    file_vide_standard.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')
    file_both_vide = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\得到的synyi_id都为空的例子.csv', 'w', encoding='utf-8')
    file_both_vide.write('CDC中诊断名称,CDC中诊断编码,CDC诊断名称对应的synyi_code,CDC诊断编码对应的标准诊断名称对应的synyi_code' + '\n')

    for index in range(len(cdc_synyi)):
        if cdc_synyi[index] != '[]' and standard_synyi[index] != '[]':
            not_blank += 1
            if cdc_synyi[index] == standard_synyi[index]:
                same += 1
                file_consis.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi[index] + ',' + standard_synyi[index] + '\n')
            else:
                file_not_consis.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi[index] + ',' + standard_synyi[index] + '\n')
        elif cdc_synyi[index] != '[]' and standard_synyi[index] == '[]':
            vide_standard += 1
            file_vide_standard.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi[index] + ',' + standard_synyi[index] + '\n')
        elif cdc_synyi[index] == '[]' and standard_synyi[index] != '[]':
            vide_cdc += 1
            file_vide_cdc.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi[index] + ',' + standard_synyi[index] + '\n')
        elif cdc_synyi[index] == '[]' and standard_synyi[index] == '[]':
            both_vide += 1
            file_both_vide.write(cause[index] + ',' + icd[index] + ',' + cdc_synyi[index] + ',' + standard_synyi[index] + '\n')

    total_not_consis = not_blank - same + vide_standard + vide_cdc + both_vide
    print('synyi_id表总长：', length_total)
    print('两个都不为空的数据：', not_blank)
    print('由code和诊断描述得到的synyi_id一致的数据：', same)
    print('由code和诊断描述得到的synyi_id不一致的数据：', not_blank - same)
    print("由code得到的synyi_id为空： ", vide_standard)
    print("由cdc得到的synyi_id为空： ", vide_cdc)
    print("由code和诊断描述得到的synyi_id都为空： ", both_vide)
    print("总的不一致的数据：", not_blank - same + vide_standard + vide_cdc + both_vide)
    # 10 24 25 26 27
    return same, total_not_consis, vide_standard, vide_cdc, both_vide, not_blank - same
# synyi_id_analysis('shanghai', '去重')

# 把synyi_code匹配.csv文件中能与标准ICD表匹配得上的例子拿出来   这个只考虑了诊断描述是完全匹配的， 但是可能虽然诊断描述对了，但他编的码是错误的
def synyi_id_icd10(file_name, code_file):
    if code_file == '去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code匹配去重text_code.csv', 'r', encoding='utf-8')
    elif code_file == '不去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code匹配不去重text_code.csv', 'r', encoding='utf-8')

    dic = get_standard_ICD("系统对照表")
    dic_list = []
    for i in dic.values():
        dic_list.extend(i)

    if code_file == '去重':
        file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code_icd_去重.csv', 'w', encoding='utf-8')
    elif code_file == '不去重':
        file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code_icd_不去重.csv', 'w', encoding='utf-8')

    for line in file:
        line = line.strip()
        if line.split(',')[0] in dic_list:
            file_out.write(line + '\n')

    file.close()
    file_out.close()


def true_false_diag_code(file_name, code_file):
    if code_file == '去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code_icd_去重.csv', 'r', encoding='utf-8')
    elif code_file == '不去重':
        file = codecs.open(path + '\内部质量同步表\\' + file_name + '\synyi_code_icd_不去重.csv', 'r', encoding='utf-8')

    if code_file == '去重':
        file_out_true = codecs.open(path + '\内部质量同步表\\' + file_name + '\去重synyi_icd表中code和诊断描述匹配对的实例.csv', 'w', encoding='utf-8')
        file_out_false = codecs.open(path + '\内部质量同步表\\' + file_name + '\去重synyi_icd表中code和诊断描述匹配错误的实例.csv', 'w', encoding='utf-8')
    elif code_file == '不去重':
        file_out_true = codecs.open(path + '\内部质量同步表\\' + file_name + '\不去重synyi_icd表中code和诊断描述匹配对的实例.csv', 'w', encoding='utf-8')
        file_out_false = codecs.open(path + '\内部质量同步表\\' + file_name + '\不去重synyi_icd表中code和诊断描述匹配错误的实例.csv', 'w', encoding='utf-8')

    dic = get_standard_ICD("系统对照表")

    for line in file:
        line = line.strip()
        cause = line.split(',')[0]
        icd = line.split(',')[1]
        if cause in dic[icd]:
            file_out_true.write(line + '\n')
        else:
            file_out_false.write(line + '\n')
    file.close()
    file_out_true.close()
    file_out_false.close()


def synyi_id_instance(file_name, code_file):
    file = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\都不为空且一致的例子.csv', 'r', encoding='utf-8')
    cdc_synyi_id = []
    standard_synyi_id = []
    cause = []
    code = []
    for line in file:
        line = line.strip()
        if '[' in line:
            cause.append(line.split(',')[0])
            code.append(line.split(',')[1])
            cdc_synyi_id.append('[' + line.split('[')[1].replace('],', ']'))
            standard_synyi_id.append('[' + line.split('[')[2])
    # print(len(cdc_synyi_id), len(standard_synyi_id))
    # cc'est possible qu'il y a des numéros pareils. Donc on remplace random.randint avec random.sample
    # random_list = [random.randint(0, len(cdc_synyi_id)-1) for _ in range(10)]
    random_list = random.sample(range(0, len(cdc_synyi_id)), 10)
    # print(random_list)

    file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\\' + code_file + '\抽样结果' + '\都不为空且一致的例子.csv', 'w', encoding='utf-8')
    file_out.write('CDC诊断名称,CDC诊断编码,CDC诊断名称对应的synyi_code,CDC诊断名称对应的NLP标准名称,CDC诊断编码对应的标准诊断名称对应的synyi_code,CDC编码对应的诊断名称对应的NLP标准名称' + '\n')

    for item in random_list:
        if cdc_synyi_id[item] == '[]':
            cdc_name = post_name(cdc_synyi_id[item])
        else:
            cdc_name = post_name(cdc_synyi_id[item])

        if standard_synyi_id[item] == '[]':
            standard_name = post_name(standard_synyi_id[item])
        else:
            standard_name = post_name(standard_synyi_id[item])
        file_out.write(str(cause[item]) + ',' + str(code[item]) + ',' + str(cdc_synyi_id[item]) + ',' + str(cdc_name) + ',' + str(standard_synyi_id[item]) + ',' + str(standard_name) + '\n')
    file_out.close()
# synyi_id_instance('beijing','去重')
# synyi_id_instance('zhejiang','去重')
# synyi_id_instance('shanghai','去重')
# synyi_id_instance('guizhou','不去重')


def only_diag_new_NLP(file_name):
    file = pd.read_csv(path + '\内部质量同步表\\' + file_name + '\只有cause的数据没有包含在去重数据中的数量.csv', encoding='utf-8')
    cause = file['诊断名称'].tolist()

    file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause的数据学synyi_id.csv', 'w', encoding='utf-8')
    file_out.write('诊断名称' + '\n')
    # for i in random_list:
    for i in range(len(cause)):
        file_out.write(cause[i] + ',' + str(post_name(post_new(cause[i]))) + '\n')


def only_diag_analysis(file_name):
    file_in = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause的数据学synyi_id.csv', 'r', encoding='utf-8')
    file_out_vide = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause学到空.csv', 'w', encoding='utf-8')
    file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause学到诊断编码.csv', 'w', encoding='utf-8')
    not_vide = 0
    vide = 0
    for line in file_in:
        line = line.strip()
        if ',' in line:
            if line.split(',')[1] == '[]':
                file_out_vide.write(line + '\n')
                vide += 1
            else:
                not_vide += 1
                file_out.write(line + '\n')
    print("仅有cause,NLP为空：", vide)
    print("仅有cause,NLP不为空：", not_vide)
    return vide, not_vide


def random_select_only_diag(file_name):
    file_in_vide = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause学到空.csv', 'r', encoding='utf-8')
    file_in = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\只有cause学到诊断编码.csv', 'r', encoding='utf-8')

    file_out_vide = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\学到空抽样.txt', 'w', encoding='utf-8')
    file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\学到诊断名称抽样.txt', 'w', encoding='utf-8')

    list_vide = file_in_vide.readlines()
    list = file_in.readlines()

    random_list = random.sample(range(0, len(list_vide)), 10)
    print(random_list)
    for item in random_list:
        file_out_vide.write(list_vide[item])

    random_list = random.sample(range(0, len(list)), 10)
    print(random_list)
    for item in random_list:
        file_out.write(list[item])


def sample_code(file_name):
    file = pd.read_csv(path + '\内部质量同步表\\' + file_name + '\只有code的数据没有包含在去重数据中的数量.csv', encoding='utf-8')
    code = file['诊断编码'].tolist()

    file_out = codecs.open(path + '\内部质量同步表\\' + file_name + '\sample\抽样只有诊断编码.csv', 'w', encoding='utf-8')

    dic = get_standard_ICD("系统对照表")

    for i in code:
        if i.upper() in dic.keys():
            for v in dic[i.upper()]:
                standard_synyi = post_new(v)
        else:
            standard_synyi = '[]'
        file_out.write(i + ',' + str(post_name(standard_synyi)) + '\n')


def report(file_name):
   two, three, four, five, six, only_cause, only_icd, twelve, thirteen = statistic_text_code(file_name)
   eleven = str(str(only_cause) + '/' + str(only_icd))

   right_five = round(five / three, 2)
   right_six = round(six / three, 2)

   sum = only_cause + only_icd

   right_eleven = str(str(round(only_cause/sum, 2)) + '/' + str(round(only_icd/sum, 2)))
   right_twelve = round(twelve/only_cause, 2)
   right_thirteen = round(thirteen/only_icd, 2)

   same, not_consist, twenty_four, twenty_five, twenty_six, twenty_seven = synyi_id_analysis(file_name, '不去重')
   ten = str(str(same) + '/' + str(not_consist))

   right_ten = str(str(round(same/three, 2)) + '/' + str(round(not_consist/three, 2)))

   right_twenty_four = round(twenty_four / three, 2)
   right_twenty_five = round(twenty_five / three, 2)
   right_twenty_six = round(twenty_six / three, 2)
   right_twenty_seven = round(twenty_seven / three, 2)

   synyi_id_icd10(file_name, '不去重')
   true_false_diag_code(file_name, '不去重')
   same, not_consist, _, _, _, _ = synyi_id_analysis(file_name, '不去重TrueFalse')
   eight = str(str(same) + '/' + str(not_consist))

   right_eight = str(str(round(same/three, 2)) + '/' + str(round(not_consist/three, 2)))

   same, not_consist, eighteen, ninteen, twenty, twenty_one = synyi_id_analysis(file_name, '去重')
   nine = str(str(same) + '/' + str(not_consist))

   right_nine = str(str(round(same/six, 2)) + '/' + str(round(not_consist/six, 2)))

   right_eighteen = round(eighteen/six, 2)
   right_ninteen = round(ninteen/six, 2)
   right_twenty = round(twenty/six, 2)
   right_twenty_one = round(twenty_one/six, 2)

   synyi_id_icd10(file_name, '去重')
   true_false_diag_code(file_name, '去重')
   same, not_consist, _, _, _, _ = synyi_id_analysis(file_name, '去重TrueFalse')
   seven = str(str(same) + '/' + str(not_consist))

   right_seven = str(str(round(same/six, 2)) + '/' + str(round(not_consist/six, 2)))

   # only_diag_new_NLP(file_name)
   vide, not_vide = only_diag_analysis(file_name)

   thirty_one = str(str(vide) + '/' + str(not_vide))
   right_thirty_one = str(str(round(vide/twelve, 2)) + '/' + str(round(vide/twelve, 2)))

   file = codecs.open(path + "\\" + file_name + "统计.csv", "w", encoding='utf-8')
   file.write(str(two) + "\n")
   file.write(str(three) + "\n")
   file.write(str(four) + "\n")
   file.write(str(five) + '\t' + str(right_five) + "\n")
   file.write(str(six) + '\t' + str(right_six) + "\n")
   file.write(str(seven) + '\t' + str(right_seven) + "\n")
   file.write(str(eight) + '\t' + str(right_eight) + "\n")
   file.write(str(nine) + '\t' + str(right_nine) + "\n")
   file.write(str(ten) + '\t' + str(right_ten) + "\n")
   file.write(str(eleven) + '\t' + str(right_eleven) + "\n")
   file.write(str(twelve) + '\t' + str(right_twelve) + "\n")
   file.write(str(thirteen) + '\t' + str(right_thirteen) + "\n")

   file.write(str(eighteen) + '\t' + str(right_eighteen) + "\n")
   file.write(str(ninteen) + '\t' + str(right_ninteen) + "\n")
   file.write(str(twenty) + '\t' + str(right_twenty) + "\n")
   file.write(str(twenty_one) + '\t' + str(right_twenty_one) + "\n")

   file.write(str(twenty_four) + '\t' + str(right_twenty_four) + "\n")
   file.write(str(twenty_five) + '\t' + str(right_twenty_five) + "\n")
   file.write(str(twenty_six) + '\t' + str(right_twenty_six) + "\n")
   file.write(str(twenty_seven) + '\t' + str(right_twenty_seven) + "\n")

   file.write(str(thirty_one) + '\t' + str(right_thirty_one) + '\n')
# report('guizhou')

# synyi_id('guizhou', '不去重text_code')
# synyi_id('guizhou', '去重text_code')
# print("# ***********1***********")
# statistic_text_code('guizhou')
# print("# ******2")
# synyi_id_analysis('guizhou', '不去重')
# synyi_id_icd10('guizhou', '不去重')
# true_false_diag_code('guizhou', '不去重')
# print("# *******3")
# synyi_id_analysis('guizhou', '不去重TrueFalse')
# print("# ***********************去重")
# print("********4")
# synyi_id_analysis('guizhou', '去重')
# synyi_id_icd10('guizhou', '去重')
# true_false_diag_code('guizhou', '去重')
# print("**************5")
# synyi_id_analysis('guizhou', '去重TrueFalse')

# print("************7")
# only_diag_new_NLP('guizhou')
# print("****************8")
# only_diag_analysis('guizhou')
# print("*************9")
# random_select_only_diag('guizhou')
# print("**************10")
# sample_code('guizhou')
