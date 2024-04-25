import requests


class Request:
    def request_api(self,method,url,headers =None,params=None,data=None,json=None,cookies =None):
        r = requests.request(method,url,headers =headers,params=params,data=data,json=json,cookies =cookies)
        r_code = r.status_code
        try:
            r_data = r.json()
        except Exception as e:
            r_data = r.text
        result = dict()
        result['code'] = r_code
        result['data'] = r_data
        return result

    def send(self,url,method,**kwargs):
        return self.request_api(method,url,**kwargs)
    def get(self,url,**kwargs):
        return self.request_api("GET",url,**kwargs)
    def post(self,url,**kwargs):
        return self.request_api("POST",url,**kwargs)
