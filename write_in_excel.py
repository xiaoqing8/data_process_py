import xlrd
import xlwt
from xlutils.copy import copy
import os.path

xlsfile = '贵州18-1207.xlsx'

rb = xlrd.open_workbook(xlsfile)
r_sheet = rb.sheet_by_index(0)
wb = copy(rb)
sheet = wb.get_sheet(0)
# sheet.write(35, 2, "string")
wb.save('my_workbook.xls')
