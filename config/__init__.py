# -*- coding:utf-8 -*-
import os

import pytest

from comm.utils.randomly import *
from comm.utils.readYaml import read_yaml_data

# 获取主目录路径
ROOT_DIR = str(os.path.realpath(__file__)).split('config')[0].replace('\\', '/')

# 获取配置文件路径
API_CONFIG = ROOT_DIR + 'config/apiConfig.yml'
RUN_CONFIG = ROOT_DIR + 'config/runConfig.yml'
DB_CONFIG = ROOT_DIR + 'config/dbConfig.yml'
DM_CONFIG = ROOT_DIR + 'config/domainConfig.yml'
CASE_DEMO = ROOT_DIR + 'config/case_demo.yaml'
THIRD_CONFIG = ROOT_DIR + 'config/thirdConfig.yaml'
# 获取运行配置信息
RC = read_yaml_data(RUN_CONFIG)
DMC = read_yaml_data(DM_CONFIG)
INTERVAL = RC['interval']
PROJECT_NAME = RC['project_name']

# 缓存数据目录(.pytest_cache)
CACHE_DIR = ROOT_DIR + '.pytest_cache'
# 接口数据目录(.chlsj文件)
DATA_DIR = ROOT_DIR + PROJECT_NAME + '/charles_data'
# 依赖文件目录(/file/)
FILE_DIR = ROOT_DIR + PROJECT_NAME + '/file'
# 测试数据目录(test.yaml)
PAGE_DIR = ROOT_DIR + PROJECT_NAME + '/api'
FLOW_DIR = ROOT_DIR + PROJECT_NAME + '/flow'
# 测试脚本目录(/script/)
SCRIPT_DIR = ROOT_DIR + PROJECT_NAME + '/script/'
# 测试脚本目录(test.py)
TEST_API_DIR = ROOT_DIR + PROJECT_NAME + '/test_api'
TEST_FLOW_DIR = ROOT_DIR + PROJECT_NAME + '/test_flow'
TEST_OTHER_DIR = ROOT_DIR + PROJECT_NAME + '/test_other'
TEST_PERFORMANCE_DIR = ROOT_DIR + PROJECT_NAME + '/test_performance'
# 测试报告目录(xml|html)
REPORT_DIR = ROOT_DIR + PROJECT_NAME + '/report'

GEN_MAP = {
    "GenPhone": generate_phone,
    "GenEmail": generate_email,
    "GenMac": generate_mac,
    "GenIp": generate_ip,
    "GenDid": generate_did,
    "GenStr": generate_str,
    "GenNowTime": generate_now_timestamp,
    "GenWeekTime": generate_week_timestamp
}
TEST_MARKERS = {
    "create": pytest.mark.create,
    "search": pytest.mark.search,
    "update": pytest.mark.update,
    "delete": pytest.mark.delete,
    "saas": pytest.mark.saas,
    "private": pytest.mark.private,
    "seal": pytest.mark.seal,
    "apicase": pytest.mark.apicase,
    "flowcase": pytest.mark.flowcase,
}

RUN_MODULE = {
    "identity": "身份管理",
    "device": "终端管理",
    "software": "软件管理",
    "application": "应用管理",
    "vpn": "VPN管理",
    "wifi": "WIFI管理",
    "baseline": "终端基线",
    "dlp": "数据防泄漏",
    "antivirus": "防病毒",
    "dynamic": "动态控制",
    "it": "IT应用",
    "configuration": "通用配置",
    "integration": "集成管理",
    "settings": "系统设置",
    "license": "权益中心",
    "versions": "版本发布"
}
