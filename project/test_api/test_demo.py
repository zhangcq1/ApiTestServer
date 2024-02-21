# -*- coding:utf-8 -*-*
import os

import allure
import pytest

from comm.unit.apiSend import send_request
from comm.unit.checkResult import check_result
from comm.unit.myCache import Cache
from comm.unit.dealCache import deal_response_info, deal_request_info
from comm.unit.initializePremise import init_premise
from comm.unit.getCaseData import get_all_case_data
from config import PAGE_DIR

file_path = os.path.realpath(__file__).replace("\\", "/")
case_yaml = file_path.replace("/test_api/", "/api/").replace(".py", ".yaml")
case_path = PAGE_DIR + "/demo"
all_case_data = get_all_case_data(case_path)
cache = Cache()


class TestAntivirus:
    @pytest.mark.parametrize("case_data", all_case_data)
    @allure.title("{case_data[test_case][describe]}")
    def test_antivirus(self, case_data):
        # 初始化请求：执行前置接口+替换关联变量
        test_case = case_data.get("test_case")
        test_info, test_case = init_premise(case_path, case_data["test_info"], test_case, cache)
        # 替换全局变量/执行脚本处理请求数据/等
        test_info, test_case = deal_request_info(cache, test_info, test_case)
        # 发送当前接口
        print("test_info:{}\ntest_case:{}".format(test_info, test_case))
        code, data, responses = send_request(test_info, test_case, get_response=True)
        print("test_info:{}\ntest_case:{}\ncode:{}\ndata:{}".format(test_info, test_case, code, data))
        # 使用模版校验接口返回
        check_result(test_case, code, data)
        # 处理异常/校验结果/设置全局变量/执行脚本等
        deal_response_info(cache, test_info, test_case, data, responses)
