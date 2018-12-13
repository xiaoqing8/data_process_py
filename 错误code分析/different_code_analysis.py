import os
import codecs
import xlrd

path = os.getcwd()
file = codecs.open(path + '\\result\DC与ICD同样的描述写的不一样的编码的编码比较.txt', 'r', encoding='utf-8')
lis = file.readlines()

# 统计诊断描述对应的code不正确的个数
# CDC_key = []
# for i in lis:
#     CDC_key.append(i.split(' ')[0])
# print(len(CDC_key))
# print(len(set(CDC_key)))
# 得到对应不到的ICD编码对
CDC = []
ICD = []
for item in lis:
    item = item.strip()
    CDC.append(item.split(' ')[0])
    ICD.append(item.split(' ')[1])
# 得到三位类目表
xls_file = xlrd.open_workbook(path + "\\3位代码类目表（ICD-10）.xls")
xls_sheet = xls_file.sheets()[0]
col_code = xls_sheet.col_values(0)[2:]
col_des = xls_sheet.col_values(1)[2:]
dic = {}
for i in range(len(col_code)):
    dic[col_code[i]] = col_des[i]
# 得到四位亚目表
xls_file_ya = xlrd.open_workbook(path + "\\4位代码亚目表（ICD-10）.xls")
xls_sheet_ya = xls_file_ya.sheets()[0]
col_code_ya = xls_sheet_ya.col_values(1)[2:]
col_des_ya = xls_sheet_ya.col_values(2)[2:]
dic_ya = {}
for j in range(len(col_code_ya)):
    dic_ya[col_code_ya[j]] = col_des_ya[j]
# 得到类目错还是亚目错; 类目错了的写明是什么类目
leimu = 0
yamu = 0
file_lei = codecs.open(path + "\类目出错.txt", 'w', encoding='utf-8')
file_lei.write('CDC code:类目; ICD code:类目' + '\n')
file_ya = codecs.open(path + "\亚目出错.txt", 'w', encoding='utf-8')
file_ya.write('CDC code:亚目; ICD code:亚目' + '\n')
for index in range(len(CDC)):
    if CDC[index][:3] != ICD[index][:3]:
        leimu += 1
        file_lei.write(CDC[index] + ": " + dic[CDC[index][:3]] + "; " + ICD[index] + ': ' + dic[ICD[index][:3]] + '\n')
    elif CDC[index][4] != ICD[index][4]:
        yamu += 1
        if CDC[index] not in dic_ya.keys() and (CDC[index] + "+") in dic_ya.keys():
            CDC[index] = CDC[index] + "+"
        elif CDC[index] not in dic_ya.keys() and (CDC[index] + "*") in dic_ya.keys():
            CDC[index] = CDC[index] + "*"
        file_ya.write(CDC[index] + ": " + dic_ya[CDC[index]] + "; " + ICD[index] + ': ' + dic_ya[ICD[index]] + '\n')
print("类目出错的code总数：", leimu)
print('亚目出错的code总数：', yamu)