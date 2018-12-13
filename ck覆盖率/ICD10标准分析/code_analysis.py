import xlrd
import os
import pandas as pd
import codecs

path = os.getcwd()

xls_yamu = xlrd.open_workbook(path + "\ICD-10亚目表.xlsx")
xls_sheet = xls_yamu.sheets()[0]
code = xls_sheet.col_values(1)
code_yamu = code[286:]


table_inter = pd.read_csv(path + '\国际英文版标准.csv', encoding='utf-8')
code_inter = table_inter['concept_code'].tolist()  # 15721

table_CDC = pd.read_csv(path + '\icd-10系统对照表.csv', encoding='utf-8')
code_CDC = table_CDC['CODE'].tolist()

file_out_inter = codecs.open(path + '\国际标准比较.txt', 'w', encoding='utf-8')
for code in code_CDC:
    if code not in code_inter:
        file_out_inter.write(code + '\n')
file_out_inter.close()

file_out_yamu = codecs.open(path + '\目前亚目表比较.txt', 'w', encoding='utf-8')
for code in code_CDC:
    if code not in code_yamu:
        file_out_yamu.write(code + '\n')
file_out_yamu.close()