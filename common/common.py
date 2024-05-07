from _datetime import datetime
import json
import os
import re
import subprocess
from utils.LogUtil import logger_init
from config.config import get_path

logger = logger_init()

def json_load(str1,str_type='json'):
    if str1 and str_type=='json':
        return json.loads(str1.encode('utf8'))
    elif str1 == '':
        return None
    else:
        return str1

def get_sql_field(sql):
    fields = re.findall(r"select (.+) from",sql)
    return fields[0].strip().split(',')

def get_allure_severity(case_severity):
    '''
    阻塞 = 'blocker'
    严重 = 'critical'
    一般 = 'normal'
    次要 = 'minor'
    建议 = 'trivial'
    :param case_severity:
    :return:
    '''
    if case_severity=='阻塞':
        return 'blocker'
    elif case_severity =='严重':
        return 'critical'
    elif case_severity =='一般':
        return 'normal'
    elif case_severity =='次要':
        return 'minor'
    elif  case_severity =='建议':
        return 'trivial'
    else:
        raise Exception('没有这个用例等级，请检查是否书写错误')

def gen_allure_report(report_org,html_report):
    logger.info("生成allure测试报告:%s" % html_report)
    try:
        category_json = os.path.join(get_path("report_org"),"categories.json")
        cp_cmd = "cp %s %s" % (category_json,report_org)
        subprocess.call(cp_cmd,shell=True)
        cmd = "allure generate %s -o %s" % (report_org,html_report)
        subprocess.call(cmd,shell=True)
    except Exception as e:
        logger.error("生成测试报告失败，错误信息: %s" % e)
        raise

class Parameterize:
    def __init__(self,pattern=r'\${(.+?)}\$'):
        self.pattern = pattern
    def contains_param(self,str1):
        return re.findall(self.pattern,str1)

    def sub(self,str1,param,data):
        pattern = r'\(.+?\)'
        new_pattern = re.sub(pattern,param,self.pattern)
        return re.sub(new_pattern,data,str1)

    def sub_all(self,str1,dict1):
        params = self.contains_param(str1)
        for param in params:
            str1 = self.sub(str1,param,dict1[param])
        return str1


    def bat_sub(self,str_list,dict1):
        result =list()
        for string in str_list:
            result.append(self.sub_all(string,dict1))
        return tuple(result)


def para_test():
    para = Parameterize()
    str1 = '{"Authorization": "Bearer ${token}$ ${name}$"}'
    str2 = '{"Authorization": "Bearer ${token}$ ${password}$"}'
    str3='{"Authorization":"haode"}'
    print(para.contains_param(str1))
    # print(para.sub(str1,'token','123'))
    d = {'token':'123456','name':'tom','password':'123456a'}
    print(para.sub_all(str1,d))
    print(type(para.sub_all(str1,d)))

    print(para.contains_param(str3))
    print(para.sub(str3,'token','12345'))
    print(para.bat_sub([str1,str2],d))
    print(para.sub_all(str3, d))




parameterize = Parameterize()
if __name__ =="__main__":
    # para_test()
    sql = 'select username,id from user_user where username="admin"'
    print(get_sql_field(sql))