import codecs
import os
import pandas as pd

path = os.getcwd()


# 将贵州新疆、北京浙江这两张表分解成一个一个的城市
def divide_cities(file_name):
    if file_name == 'guizhou_xinjiang':
        file_in = codecs.open(path + '\data\\' + file_name + '.csv', 'r', encoding='utf-8')
        file_xinjiang = codecs.open(path + '\data\\xinjiang.csv', 'w', encoding='utf-8')
        file_guizhou = codecs.open(path + '\data\\guizhou.csv', 'w', encoding='utf-8')
        file_other = codecs.open(path + '\data\\other.csv', 'w', encoding='utf-8')
        file_xinjiang.write('CARDID,ZONECODE,CARDCODE,PERSONAL_TYPE,PATIENTNAME,SEXNAME,WOMAN_TYPE,IDCARD_TYPE,ID,BIRTHDAY,DEADDATE,AGRUNIT,COUNTRY,NATIONNAME,MARRIAGENAME,WORKTYPENAME,EDULEVELNAME,PLACETYPE,ADDR,ADDZONECODE,ADDCUNCODE,ADDCUNNAME,AREATYPE,REGISTERADDR,REGISTERZONECODE,REG_VILLAGE_NAME,REG_VILLAGE,WORKPLACE,DEADZONENAME,FOLKNAME,FOLKTEL,FOLKADDR,A_CAUSE,A_ICD10,A_SCOPETIME,A_SCOPETIMEUNIT,B_CAUSE,B_ICD10,B_SCOPETIME,B_SCOPETIMEUNIT,C_CAUSE,C_ICD10,C_SCOPETIME,C_SCOPETIMEUNIT,D_CAUSE,D_ICD10,D_SCOPETIME,D_SCOPETIMEUNIT,OTHER1_CAUSE,OTHER1_ICD10,BASECAUSE,BSICD10,DORGLEVEL,DIAGNOSEBY,DOCTOR,HOSPITALNO,FILLDATE,MAYBE_CASE,ORGCODE,ORGNAME,INFORMANT,RELATIONSHIP,INFORMANTADDR,INFORMANTTEL,INVESTIGATEDATE,INVESTIGATOR,DELETETIME,INTIME,USERID,FLAG,VALIDDATE,AUDIT_USER,FVALIDDATE,AUDIT_NFLAG,AUDIT_NCAUSE,STATE,DATASOURCE,ECOMTYPE,ECOMTYPENAME,REGISTERCUNNAME,VALIDATE,REGISTERCUNCODE,code,rcode,age,ICD3,icd,gender,deadzonename1,dorglevel1,provcode' + '\n')
        file_guizhou.write('CARDID,ZONECODE,CARDCODE,PERSONAL_TYPE,PATIENTNAME,SEXNAME,WOMAN_TYPE,IDCARD_TYPE,ID,BIRTHDAY,DEADDATE,AGRUNIT,COUNTRY,NATIONNAME,MARRIAGENAME,WORKTYPENAME,EDULEVELNAME,PLACETYPE,ADDR,ADDZONECODE,ADDCUNCODE,ADDCUNNAME,AREATYPE,REGISTERADDR,REGISTERZONECODE,REG_VILLAGE_NAME,REG_VILLAGE,WORKPLACE,DEADZONENAME,FOLKNAME,FOLKTEL,FOLKADDR,A_CAUSE,A_ICD10,A_SCOPETIME,A_SCOPETIMEUNIT,B_CAUSE,B_ICD10,B_SCOPETIME,B_SCOPETIMEUNIT,C_CAUSE,C_ICD10,C_SCOPETIME,C_SCOPETIMEUNIT,D_CAUSE,D_ICD10,D_SCOPETIME,D_SCOPETIMEUNIT,OTHER1_CAUSE,OTHER1_ICD10,BASECAUSE,BSICD10,DORGLEVEL,DIAGNOSEBY,DOCTOR,HOSPITALNO,FILLDATE,MAYBE_CASE,ORGCODE,ORGNAME,INFORMANT,RELATIONSHIP,INFORMANTADDR,INFORMANTTEL,INVESTIGATEDATE,INVESTIGATOR,DELETETIME,INTIME,USERID,FLAG,VALIDDATE,AUDIT_USER,FVALIDDATE,AUDIT_NFLAG,AUDIT_NCAUSE,STATE,DATASOURCE,ECOMTYPE,ECOMTYPENAME,REGISTERCUNNAME,VALIDATE,REGISTERCUNCODE,code,rcode,age,ICD3,icd,gender,deadzonename1,dorglevel1,provcode' + '\n')

        count_id = 0
        count = 0
        count_total = 0

        for line in file_in:
            line = line.strip()
            if line.split(',')[1][0:2] == '65':
                file_xinjiang.write(line + '\n')
            elif line.split(',')[1][0:2] == '52':
                file_guizhou.write(line + '\n')
            else:
                if line.split(',')[8][0:2] == '52' or line.split(',')[8][0:2] == '65':
                    count_id += 1
                if line.split(',')[8][0:2] != '^':
                    count += 1
                count_total += 1
                file_other.write(line + '\n')
                print('贵州新疆表中剩下的数据身份证号不为空的比例：', count/count_total)
                print('新疆贵州地区的身份证号的比例：', count_id/count)
    elif file_name == 'beijing_zhejiang':
        file_in = codecs.open(path + '\data\\' + file_name + '.csv', 'r', encoding='utf-8')
        file_beijing = codecs.open(path + '\data\\beijing.csv', 'w', encoding='utf-8')
        file_other = codecs.open(path + '\data\\除了北京的其他数据.csv', 'w', encoding='utf-8')

        for line in file_in:
            line = line.strip()
            if line.split(',')[1][0:2] == '11':
                file_beijing.write(line + '\n')
            else:
                file_other.write(line + '\n')
# divide_cities('beijing_zhejiang')


# 在上一步divede_cities步骤之后由于只筛选出了北京浙江表中的北京数据，因此这个函数中要
# 用到剩余的数据以及浙江17原始数据库来得到能从北京浙江总表中抽取出的浙江数据
def get_zhejiang_data():
    count_other = 0
    count_zhejiang = 0
    count = 0
    file_in = codecs.open(path + '\data\除了北京的其他数据.csv', 'r', encoding='utf-8')
    file_zhejiang = pd.read_csv(path + '\data\浙江17原始数据库.csv', encoding='utf-8')['报告卡编号'].tolist()
    file_out = codecs.open(path + '\data\zhejiang.csv', 'w', encoding='utf-8')
    file_other = codecs.open(path + '\data\除了北京浙江的其他数据.csv', 'w', encoding='utf-8')
    for line in file_in:
        count += 1
        line = line.strip()
        if line.split(',')[2] in file_zhejiang:
            count_zhejiang += 1
            file_out.write(line + '\n')
        else:
            count_other += 1
            file_other.write(line + '\n')
    print(count, count_zhejiang, count_other)  # 310350（总） 308777（浙江） 1573（其他地区）
# get_zhejiang_data()


# 把第一次贵州新疆表分类过程中没有找到分类对象的数据重新进行考察
def update_guizhou_xinjiang_divides():
    file_in = codecs.open(path + '\data\other.csv', 'r', encoding='utf-8')
    file_guizhou_update = codecs.open(path + '\data\guizhou_update.csv', 'w', encoding='utf-8')
    file_xinjiang_update = codecs.open(path + '\data\\xinjiang_update.csv', 'w', encoding='utf-8')
    file_other_update = codecs.open(path + '\data\\other_update.csv', 'w', encoding='utf-8')

    for line in file_in:
        line = line.strip()
        if line.split(',')[8][0:2] == '52' or line.split(',')[19][0:2] == '52' :
            file_guizhou_update.write(line + '\n')
        elif line.split(',')[8][0:2] == '65' or line.split(',')[19][0:2] == '65':
            file_xinjiang_update.write(line + '\n')
        else:
            file_other_update.write(line + '\n')


def update_beijing_zhejiang_divides():
    file_in = codecs.open(path + '\data\除了北京浙江的其他数据.csv', 'r', encoding='utf-8')
    file_beijing_update = codecs.open(path + '\data\\beijing_update.csv', 'w', encoding='utf-8')
    file_zhejiang_update = codecs.open(path + '\data\\zhejiang_update.csv', 'w', encoding='utf-8')
    file_other_update = codecs.open(path + '\data\\除了北京浙江的其他数据_update.csv', 'w', encoding='utf-8')

    for line in file_in:
        line = line.strip()
        if line.split(',')[8][0:2] == '11' or line.split(',')[19][0:2] == '11' :
            file_beijing_update.write(line + '\n')
        elif line.split(',')[8][0:2] == '33' or line.split(',')[19][0:2] == '33':
            file_zhejiang_update.write(line + '\n')
        else:
            file_other_update.write(line + '\n')

# update_beijing_zhejiang_divides()
# divide_cities('guizhou_xinjiang')
# update_guizhou_xinjiang_divides()