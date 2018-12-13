import os
import codecs
import pandas as pd


def get_string(file_name):
    path = os.getcwd()
    # file = codecs.open(path + '\编码匹配\\' + file_name + '\编码匹配.csv', )
    file = pd.read_csv(path + '\编码匹配\\' + file_name + '\编码匹配.csv', encoding='utf-8')

    cause_list = file['数据集中诊断名称'].tolist()
    ICD_list = file['CDC用的ICD表以及2011年ICD表中的诊断名称'].tolist()
    return cause_list, ICD_list


def lcs_len(a, b):
    '''    a, b: strings    '''
    n = len(a)
    m = len(b)
    l = [([0] * (m + 1)) for i in range(n + 1)]
    direct = [([0] * m) for i in range(n)]  # 0 for top left, -1 for left, 1 for top

    for i in range(n + 1)[1:]:
        for j in range(m + 1)[1:]:
            if a[i - 1] == b[j - 1]:
                l[i][j] = l[i - 1][j - 1] + 1
            elif l[i][j - 1] > l[i - 1][j]:
                l[i][j] = l[i][j - 1]
                direct[i - 1][j - 1] = -1
            else:
                l[i][j] = l[i - 1][j]
                direct[i - 1][j - 1] = 1
    return l, direct


def get_lcs(direct, a, i, j):
    '''    direct: martix of arrows
    a: the string regarded as row
    i: len(a) - 1, for initialization
    j: len(b) - 1, for initialization
    '''
    lcs = []
    get_lcs_inner(direct, a, i, j, lcs)
    return lcs


def get_lcs_inner(direct, a, i, j, lcs):
    if i < 0 or j < 0:
        return
    if direct[i][j] == 0:
        get_lcs_inner(direct, a, i - 1, j - 1, lcs)
        lcs.append(a[i])

    elif direct[i][j] == 1:
        get_lcs_inner(direct, a, i - 1, j, lcs)
    else:
        get_lcs_inner(direct, a, i, j - 1, lcs)


def similarity(a, b):
    if len(a) > len(b):
        tmp = a
        a = b
        b = tmp
    # print(a, b)
    l, direct = lcs_len(a, b)
    lcs = get_lcs(direct, a, len(a) - 1, len(b) - 1)
    len_lcs = l[len(a)][len(b)]
    # print("the length of lcs is:", len_lcs)
    # print("one of the lcs:", "".join(lcs))
    sim = round((((len_lcs + 1) * len_lcs)/(len(a)*len_lcs + len(b))), 3)
    return sim


if __name__ == "__main__":
    # a = "重度营养不良"
    a = "风湿性主动脉瓣狭窄伴有关闭不全"
    b = "风湿性主动脉瓣狭窄，伴有闭锁不全"

    print(similarity(a, b))

    # cause_list_original, ICD_list = get_string('guizhou_xinjiang')
    # cause_list = []
    # for value in cause_list_original:
    #     value = value.replace(',', '，')
    #     cause_list.append(value)
    #
    # sim_list = []
    # for index in range(len(cause_list)):
    #     sim_list.append(similarity(cause_list[index], ICD_list[index]))
    # print(len(sim_list))
    # count = 0
    # for index in range(len(sim_list)):
    #     if sim_list[index] > 0.9:
    #         count += 1
    #         print(sim_list[index], cause_list[index], ICD_list[index])
    # print(count)