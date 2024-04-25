# Create your tests here.
import requests
import json
import pytest

from config.config import config
from utils.RequestUtil import Request
from utils.LogUtil import logger_init
from utils.AssertUtil import Assert
from utils.DbUtil import db
from utils.LogUtil import my_log

#
base_url = config.url or 'http://127.0.0.1:8000/'
logger = logger_init()
my_assert = Assert()
class Test_Taotao(object):
    def setup_class(self):
        self.base_url = base_url
        self.headers = ''
        self.request = Request()
        logger.debug("base_url: %s" %  self.base_url)

    @my_log
    def test_login(self):
        url = self.base_url + "login/"
        data = {'username':"admin","password":"123456"}
        logger.info("send post request: url: %s, data: %s" % (url,data))
        r = self.request.post(url,data=data)
        logger.debug("http response: %s" % r)
        self.token = r['data']['data']['token']
        self.headers = {"Authorization": "Bearer " + self.token}
        logger.debug("token: %s" % self.token)
        #assert code
        my_assert.assert_code(r['code'],200)
        #assert body: token field
        expected = r'"token":'
        my_assert.assert_contains(r,expected)
        #assert body fields
        fields = {k:v for k,v in r['data'].items() if k in ("username",'user_id')}
        print(fields)
        db_data = db.fetchone("select username,id from user_user")
        my_assert.assert_body_fields(fields,db_data)

    @my_log
    def test_get_users(self):
        url = self.base_url + "users/"
        logger.info("send get request: url: %s"  % url)
        r = self.request.get(url, headers=self.headers)
        logger.debug("http response: %s" % r)
        assert False

    @pytest.mark.flaky(reruns=3,reruns_delay=1)
    @my_log
    def test_get_groups(self):
        url = self.base_url + "groups/"
        logger.info("send get request: url: %s" % url)
        r = self.request.get(url, headers=self.headers)
        logger.debug("http response: %s" % r)
        assert False

    @my_log
    def get_user(self):
        url = self.base_url + "user/"
        logger.info("send get request: url: %s" % url)
        r = self.request.get(url, headers=self.headers)
        logger.debug("http response: %s" % r)

    @my_log
    def get_cart(self):
        url = self.base_url + "carts/"
        logger.info("send get request: url: %s" % url)
        r = self.request.get(url, headers=self.headers)
        logger.debug("http response: %s" % r)

    @my_log
    def get_products(self):
        url = self.base_url + "products/"
        json = {
            'category':"1",
            'ordering':'sales',
            'page_size':"5",
            'page': "2"
        }
        logger.info("send get request: url: %s json: %s" % (url,json))
        r = self.request.get(url, headers=self.headers,json=json)
        logger.debug("http response: %s" % r)

    @my_log
    def create_items(self):
        url = self.base_url + "items/"
        json = {
            'customer': '3',
            'product': '2',
            'count': '10011',
            'selected': 'True',
            'cart': '1',
            'order':'',
        }
        logger.info("send post request: url: %s json: %s" % (url, json))
        r = self.request.post(url, headers=self.headers, json=json)
        logger.debug("http response: %s" % r)

    @my_log
    def save_order(self):
        url = self.base_url + "orders/"
        json ={
            'customer':'2',
            'address':'1',
            'express':'1',
            'express_cost':12,
            'total':12000,
            'pay_method':1,
        }
        logger.info("send post request: url: %s json: %s" % (url, json))
        r = self.request.post(url, headers=self.headers,json=json)
        logger.debug("http response: %s" % r)

# if __name__ == "__main__":
#
#     t.login()
#     t.get_users()
#     t.get_groups()
#     t.get_user()
#     t.get_cart()
#     t.get_products()
#     t.create_items()
#     t.save_order()