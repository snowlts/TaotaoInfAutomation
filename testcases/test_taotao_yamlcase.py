import pytest



from config.config import config
from data.DataLoader import testcases_yml
from utils.RequestUtil import Request
from utils.LogUtil import logger_init
from utils.AssertUtil import Assert
from utils.DbUtil import db
from utils.LogUtil import my_log

base_url = config.url or 'http://127.0.0.1:8000/'
logger = logger_init()
my_assert = Assert()

class Test_Taotao(object):
    def setup_class(self):
        self.base_url = base_url
        self.headers = ''
        self.request = Request()
        logger.debug("base_url: %s" %  self.base_url)


    @pytest.mark.parametrize('testcase',testcases_yml.data)
    def test_login(self,testcase):
        url = self.base_url + testcase['path']
        data = testcase['data']
        logger.info("send post request: url: %s, data: %s" % (url,data))
        r = self.request.post(url,data=data)
        logger.debug("http response: %s" % r)
        # self.token = r['data']['data']['token']
        # self.headers = {"Authorization": "Bearer " + self.token}
        # logger.debug("token: %s" % self.token)
        code,body,expected = r['code'],r['data'],testcase['expected']
        exp_code,exp_body,exp_contains,exp_fields,exp_sql = expected.get('code',None),expected.get('body',None),expected.get('contains',None),expected.get('fields',None),expected.get('sql',None)
        # assert code
        if exp_code:
            my_assert.assert_code(code,exp_code)
        #assert body
        if exp_body:
            my_assert.assert_body(body,exp_body)
        if exp_contains:
            for c in exp_contains:
                print(c)
                my_assert.assert_contains(body,c)
        if exp_fields:
            fields = {k:v for k,v in body.items() if k in exp_fields.keys()}
            my_assert.assert_body_fields(fields, exp_fields)
        if exp_sql:
            fields = {k:v for k,v in body.items() if k in exp_fields.keys()}
            db_data = db.fetchone("select username,id from user_user")
            my_assert.assert_body_fields(fields,db_data)