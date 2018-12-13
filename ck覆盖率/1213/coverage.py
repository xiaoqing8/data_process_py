import codecs
import os
import pandas as pd
import xlrd

file_out = codecs.open('D:\stage\data_process_系统对照表\ck覆盖率\不在标准中的诊断名称.txt', 'w', encoding='utf-8')
# ****************************得到所有的诊断名称*********************
table = pd.read_csv('D:\stage\data_process_系统对照表\dataset\死因总表.csv', encoding='utf-8')

a = table['A_CAUSE'].tolist()
b = table['B_CAUSE'].tolist()
c = table['C_CAUSE'].tolist()
d = table['D_CAUSE'].tolist()
other = table['OTHER1_CAUSE'].tolist()
base = table['BASECAUSE'].tolist()

cause_original = a + b + c + d + other + base
print(len(cause_original))
cause = []
for i in cause_original:
    if i != '^':
        cause.append(i)

cause_dedup = set(cause)

print("不为空的诊断描述一共有：", len(cause))
print("不为空的诊断描述去重后有：", len(cause_dedup))

# *****************************得到CDC新的标准************************
stan_new_cdc = pd.read_csv('D:\stage\data_process_系统对照表\data\icd-10系统对照表_1.csv', encoding='utf-8')['ICDCNNAME'].tolist()
print("CDC 新标准的长度：", len(stan_new_cdc))

# *****************************得到CDC旧的标准************************
XLSX_FIlE = 'D:\stage\data_process_系统对照表\data\ICD-10类目总表.xlsx'
SHEET_NAME = 'Sheet1'
workbook = xlrd.open_workbook(XLSX_FIlE)
sheet = workbook.sheet_by_name(SHEET_NAME)
stan_old_cdc_original = sheet.col_values(1)
stan_old_cdc = []
for item in stan_old_cdc_original:
    stan_old_cdc.append(item.replace(' *', ''))
print("CDC 旧标准的长度：", len(stan_old_cdc))

# *****************************CDC新旧标准融合************************
stan_cdc = stan_new_cdc + stan_old_cdc

# ******************CDC诊断文本在新旧标准中的比例************************
count_cdc = 0
lis_not_in_stan_cdc = []
for i in cause_dedup:
    if i in stan_cdc:
        count_cdc += 1
    else:
        lis_not_in_stan_cdc.append(i)

print("全体数据集中在CDC标准中的个数：", count_cdc)
print("全体数据集中在CDC标准中的比例:", count_cdc/len(cause_dedup))

# ******************得到目前使用的亚目表中的名称************************
count_yamu = 0
not_in_yamu = []
xls_yamu = xlrd.open_workbook('D:\stage\data_process_系统对照表\ck覆盖率\ICD10标准分析\ICD-10亚目表.xlsx')
xls_sheet = xls_yamu.sheets()[0]
code_yamu = xls_sheet.col_values(2)
# ******************CDC诊断文本不在新旧标准中，但在亚目表中的比例************************
for i in lis_not_in_stan_cdc:
    if i in code_yamu:
        count_yamu += 1
    else:
        # file_out.write(i + '\n')
        not_in_yamu.append(i)
print("不在CDC标准中但在亚目表中的个数：", count_yamu)
print("在CDC标准及亚目表中的比例:", (count_yamu + count_cdc)/len(cause_dedup))


# ******************得到国标版表中的名称************************
count_GBT = 0
not_in_GBT = []
xls_GBT = xlrd.open_workbook('D:\stage\data_process_系统对照表\ck覆盖率\\1213\国内ICD10汇总.xlsx')
xls_sheet = xls_GBT.sheet_by_name('GBT-14396-2016')
code_GBT = xls_sheet.col_values(2)
# ******************CDC诊断文本不在新旧标准中、亚目表但在国标版中的比例************************
for i in not_in_yamu:
    if i in code_GBT:
        count_GBT += 1
    else:
        file_out.write(i + '\n')
        not_in_GBT.append(i)
print("不在CDC标准、亚目表中但在国标版中的个数：", count_GBT)
print("在CDC标准及亚目表中及国标版中的比例:", (count_yamu + count_cdc + count_GBT)/len(cause_dedup))


