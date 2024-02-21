# -*- coding:utf-8 -*-
import json
import logging
import os
import urllib.parse

from comm.utils.readYaml import write_yaml_file, read_yaml_data
from config import API_CONFIG, PROJECT_NAME, DMC


# 从session中解析出系统配置信息
def init_api_conf(har_ct):
    host = har_ct["host"]
    port = har_ct["actualPort"]
    headers = har_ct["request"]["header"]['headers']
    # 定义项目api通过配置
    proj_conf = dict()
    proj_conf['timeout'] = 10
    proj_conf['scheme'] = har_ct["scheme"]
    proj_conf['host'] = host + ':' + str(port)
    simp_header = dict()
    for header in headers:
        # 去除基础请求头
        base_header = ['Host',
                       'Content-Length',
                       'User-Agent',
                       'Origin',
                       'Referer',
                       'Connection',
                       'Accept',
                       'Accept-Encoding',
                       'Accept-Language']
        if header['name'] not in base_header:
            simp_header[header['name']] = header['value']

    # 判断是否存在自定义消息头
    if simp_header:
        proj_conf['headers'] = simp_header
    else:
        proj_conf['headers'] = None

    # 检查是否已存在项目配置信息，没有则写入
    run_conf = read_yaml_data(API_CONFIG)
    if run_conf:
        if PROJECT_NAME not in run_conf:
            run_conf[PROJECT_NAME] = proj_conf
            write_yaml_file(API_CONFIG, run_conf)
    else:
        api_conf = dict()
        api_conf[PROJECT_NAME] = proj_conf
        write_yaml_file(API_CONFIG, api_conf)


def parse_request_parameter(har_ct):
    # 解析请求报文： 将请求体解析为一个数据对象
    parameter = dict()
    method = har_ct["method"]
    try:
        if method in 'POST':
            try:
                parameter_list = urllib.parse.unquote(har_ct["request"]["body"]["text"])
            except KeyError:
                parameter_list = []
        elif method in 'PUT':
            parameter_list = har_ct["request"]["body"]["text"]
        elif method in 'DELETE':
            parameter_list = urllib.parse.unquote(har_ct["query"])
        else:
            parameter_list = har_ct["query"]
        if parameter_list:
            try:
                if "&" in parameter_list:
                    for key in parameter_list.split("&"):
                        val = key.split("=")
                        parameter[val[0]] = val[1]
                elif "=" in parameter_list:
                    val = parameter_list.split("=")
                    parameter[val[0]] = val[1]
                else:
                    parameter = json.loads(parameter_list)
            except:
                parameter = json.loads(parameter_list)
        else:
            parameter = None
        return parameter

    except Exception as e:
        parameter = None
        logging.error("未找到parameter: %s" % e)
        raise e


def init_test_case(har_ct, module_path, parameter, file_name):
    title = file_name
    # 定义测试用例
    test_case = dict()
    test_case["summary"] = title
    test_case["describe"] = 'test_' + title
    test_case["script"] = None
    test_case["order"] = 9999
    test_case["markers"] = ["#saas", "#private"]
    test_case["set_cache"] = None
    test_case["replace_cache"] = None
    test_case["parameter"] = parameter

    # 定义请求返回信息： 根据请求信息，编写请求校验参数&校验类型
    response_code = har_ct["response"]["status"]
    try:
        response_body = har_ct["response"]["body"]["text"]
    except Exception as error:
        print("response_body 获取失败:{}".format(error))
        response_body = '{"code":0}'
    check = dict()
    check["check_type"] = 'check_json'
    check["expected_code"] = response_code
    expected_request = json.loads(response_body)
    check["expected_result"] = expected_request
    test_case["check_body"] = check
    return test_case


def write_case_yaml(har_path):
    """循环读取接口数据文件

    :param har_path: Charles导出文件路径
    :return:
    """
    case_file_list = list()
    logging.info("读取抓包文件主目录: {}".format(har_path))
    har_list = os.listdir(har_path)
    error_list = []
    for each in har_list:
        # ext_name = os.path.splitext(each)[1]
        file_name, ext_name = os.path.splitext(each)
        try:
            if ext_name == '.chlsj':
                logging.info("读取抓包文件: {}".format(each))
                file_path = har_path + '/' + each
                # 用例目录名：
                caseDirName = each.split('_')[0]
                with open(file_path, 'r', encoding='utf-8') as f:
                    har_cts = json.loads(f.read())
                    har_ct = har_cts[0]
                    # 获取接口基本信息
                    method = har_ct["method"]
                    port = har_ct["actualPort"]
                    path = har_ct["path"]
                    title = file_name
                    module = path.split("/")[-2].replace('-', '')
                    module_path = har_path.split('charles_data')[0] + 'api/' + caseDirName
                    # 创建模块目录
                    try:
                        os.makedirs(module_path)
                    except:
                        pass

                    # 初始化api配置
                    init_api_conf(har_ct)
                    # 解析请求参数
                    parameter = parse_request_parameter(har_ct)
                    # 初始化测试用例 ： 当前请求的详细信息，路径，请求体信息，文件名
                    test_case = init_test_case(har_ct, module_path, parameter, file_name)
                    # 定义测试信息： 当前请求的上下文，file cookies premise设置为空了
                    test_info = dict()
                    test_info["title"] = module
                    test_info["host"] = '${host}'
                    test_info["route_type"] = '${route_type}'
                    test_info["scheme"] = '${scheme}'
                    test_info["method"] = method
                    if port == "8443" or "admin" in path:
                        test_info["address"] = ':${admin_port}' + path
                        test_info["address_saas"] = ':${admin_port}' + path
                        test_case["summary"] = "测试【】接口".format(path)
                    else:
                        test_info["address"] = ':${fe_port}' + path
                        test_info["address_saas"] = ':${fe_port}' + path
                    test_info["mime_type"] = har_ct["request"]["mimeType"]
                    test_info["headers"] = '${headers}'
                    test_info["timeout"] = '${timeout}'
                    test_info["file"] = False
                    test_info["cookies"] = False
                    test_info["premise"] = False
                    # 合并测试信息、测试用例
                    case_list = dict()
                    case_list["test_info"] = test_info
                    case_list["test_case"] = [test_case]
                    # 写入测试用例(存在则忽略)
                    headIndex = len(caseDirName)
                    case_name = 'test' + title[headIndex:] + '.yaml'
                    case_file = module_path + '/' + case_name

                    if not os.path.exists(case_file):
                        logging.info("生成用例文件: {}".format(case_file))
                        write_yaml_file(case_file, case_list)
                    case_file_list.append(case_file)
        except Exception as error:
            print(error)
            error_list.append(file_name)
    logging.info("失败文件为: {}".format(error_list))
    return case_file_list


if __name__ == '__main__':
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    print('测试用例列表: ', write_case_yaml(real_path + '/charles_data'))
