from datetime import datetime
import os
import pytest

from common.common import gen_allure_report
from config.config import get_path
from utils.EmailUtils import mail
from utils.LogUtil import logger_init

logger = logger_init()

if __name__ == "__main__":
    # report_dir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # report_org = os.path.join(get_path('report_org'),report_dir)
    # html_report = os.path.join(get_path('html_report'),report_dir)
    report_org = get_path('report_org')
    html_report = get_path('html_report')
    pytest.main(['-s','--reruns',3,'--reruns-delay',1,'testcases/test_taotao_excel.py',"--alluredir",report_org,'--clean-alluredir'])
    # gen_allure_report(report_org,html_report)
    # report_link = "http://localhost:63342/TaotaoInfAutomation/report/html/{}/index.html".format(report_dir)
    # logger.info("send email")
    # mail.send("测试报告",report_link)