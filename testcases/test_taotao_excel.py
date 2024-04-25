import requests
import json
import pytest

from config.config import config
from data.DataLoader import testcases
from utils.RequestUtil import Request
from utils.LogUtil import logger_init
from utils.AssertUtil import Assert
from utils.DbUtil import db
from utils.LogUtil import my_log

from common.common import parameterize,json_load,get_sql_field
#
base_url = config.url or 'http://127.0.0.1:8000/'
logger = logger_init()
my_assert = Assert()
class Test_Taotao(object):
    def setup_class(self):
        self.base_url = base_url
        self.request = Request()
        logger.debug("base_url: %s" %  self.base_url)

    def _run_case(self,testcase):
        logger.info("用例编号:%s,接口:%s,测试点:%s" % (testcase['用例编号'], testcase['接口'], testcase['测试点']))
        data, headers, cookies = testcase['请求参数'], testcase['headers'], testcase['cookies']

        #运行前置用例，并获取返回值
        if testcase['前置条件']:
            dep_data =self._run_dependent_case(testcase['前置条件'])
            #参数替换
            data,headers,cookies = parameterize.bat_sub([data,headers,cookies],dep_data)
        data,headers,cookies = json_load(data,testcase['参数类型']),json_load(headers),json_load(cookies)

        ##发送http请求
        url = self.base_url + testcase['path']
        method= testcase['请求方法']
        logger.info("send %s request: url: %s, data: %s" % (method, url, data))
        r = self.request.send(url, method, data=data,headers=headers,cookies=cookies)

        #获取返回值，并return
        logger.debug("http response: %s" % r)
        return r

    def _run_dependent_case(self,case_id):
        #根据case_id获取用例
        testcase = testcases.data[case_id]
        r = self._run_case(testcase)
        return r['data']

    def _assert_case(self,http_response,testcase):
        code, body = http_response['code'], http_response['data']
        exp_code, exp_body, exp_contains, exp_fields, exp_sql = (int(testcase['期望返回值code']),
                                                                 testcase['期望返回值body'],
                                                                 testcase['期望返回值contains'],
                                                                 testcase['期望返回值字段值'],
                                                                 testcase['通过数据库验证'])

        # assert code
        if exp_code:
            my_assert.assert_code(code, exp_code)
        # assert body
        if exp_body:
            my_assert.assert_body(body, exp_body)
        if exp_contains:
            for c in exp_contains.split(";"):
                print(c)
                my_assert.assert_contains(body, c)
        if exp_fields:
            exp_fields = json.loads(exp_fields.encode('utf-8'))
            fields = {k: v for k, v in body.items() if k in exp_fields.keys()}
            print(exp_fields,fields)
            print(body.items())
            my_assert.assert_body_fields(fields, exp_fields)
        if exp_sql:
            sql_fields = get_sql_field(exp_sql)
            fields = {k: v for k, v in body.items() if k in sql_fields}
            db_data = db.fetchall(testcase['通过数据库验证'])[0]
            print('db:', db_data)
            my_assert.assert_body_fields(fields, db_data)
    @pytest.mark.parametrize('testcase',testcases.data.values())
    def test_run(self,testcase):
        http_response =self._run_case(testcase)
        self._assert_case(http_response,testcase)

