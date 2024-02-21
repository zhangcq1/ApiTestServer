# -*- coding:utf-8 -*-
import json
import logging
import os
import time
from json import JSONDecodeError

from comm.unit import apiSend, readRelevance, replaceRelevance
from comm.utils import readYaml
from config import PAGE_DIR, PROJECT_NAME, API_CONFIG


def read_json(summary, json_obj, case_path):
    """
    校验内容读取
    :param summary: 用例名称
    :param json_obj: json文件或数据对象
    :param case_path: case路径
    :return:
    """
    if isinstance(json_obj, dict):
        return json_obj
    elif isinstance(json_obj, list):
        return json_obj
    else:
        try:
            # 读取json文件指定用例数据
            case_path = "/".join(case_path.split('/')[:-1])
            with open(case_path + '/' + json_obj, "r", encoding="utf-8") as js:
                data_list = json.load(js)
                for data in data_list:
                    if data['summary'] == summary:
                        return data['body']
        except FileNotFoundError:
            raise Exception("用例关联文件不存在\n文件路径： %s" % json_obj)
        except JSONDecodeError:
            raise Exception("用例关联的文件有误\n文件路径： %s" % json_obj)


def init_premise(case_path, test_info, case_data, cache):
    """用例前提条件执行，提取关键值
    :param test_info: 测试信息
    :param case_data: 用例数据cache
    :param case_path: 用例路径
    :param cache: pytest 缓存
    :return:
    """
    # 获取项目公共关联值
    aconfig = readYaml.read_yaml_data(API_CONFIG)
    __relevance = aconfig[PROJECT_NAME]
    if __relevance.get("other") and "fe_port" in test_info.get("address"):
        test_info["host"] = __relevance.get("other")
    # 处理测试信息
    __relevance["cache"] = cache
    __relevance["case_path"] = case_path
    test_info = replaceRelevance.replace(test_info, __relevance)
    case_data = replaceRelevance.replace(case_data, __relevance)
    logging.debug("测试信息处理结果：{}".format(test_info))
    # 处理Cookies
    if test_info['cookies']:
        cookies = aconfig[PROJECT_NAME]['cookies']
        logging.debug("请求Cookies处理结果：{}".format(cookies))
    # 判断是否存在前置接口
    # pre_case_path_info = test_info["premise"]
    # if pre_case_path_info:
    #     pre_case_path = pre_case_path_info
    #     pointer = "test_case"
    #     count = 0
    #     if "[" in pre_case_path_info:
    #         pre_case_path = pre_case_path_info.split("[")[0]
    #         pointer = pre_case_path_info.split("[")[-1].strip('[').strip(']')
    #     if "][" in pre_case_path_info:
    #         pre_case_path = pre_case_path_info.split("[")[0]
    #         pointer = pre_case_path_info.split("[")[1].strip('[').strip(']')
    #         count = int(pre_case_path_info.split("[")[2].strip('[').strip(']'))
    #
    #     # 获取前置接口用例
    #     logging.info("获取前置接口测试用例：{}".format(pre_case_path))
    #     pre_case_yaml = PAGE_DIR + pre_case_path
    #     pre_case_path = os.path.dirname(pre_case_yaml)
    #
    #     pre_case_dict = readYaml.read_yaml_data(pre_case_yaml)
    #     pre_test_info = pre_case_dict['test_info']
    #     pre_case_data = pre_case_dict[pointer][count]
    #     # 判断前置接口是否也存在前置接口
    #     if pre_test_info["premise"]:
    #         init_premise(pre_test_info, pre_case_data, pre_case_path, cache)
    #
    #     for i in range(3):
    #         # 处理前置接口测试信息
    #         pre_test_info = replaceRelevance.replace(pre_test_info, __relevance)
    #         logging.debug("测试信息处理结果：{}".format(pre_test_info))
    #         # 处理前置接口Cookies
    #         if pre_test_info['cookies']:
    #             cookies = aconfig[PROJECT_NAME]['cookies']
    #             logging.debug("请求Cookies处理结果：{}".format(cookies))
    #         # 处理前置接口入参：获取入参-替换关联值-发送请求
    #         pre_parameter = read_json(pre_case_data['summary'], pre_case_data['parameter'], pre_case_path_info)
    #         pre_parameter = replaceRelevance.replace(pre_parameter, __relevance)
    #         pre_case_data['parameter'] = pre_parameter
    #         logging.debug("请求参数处理结果：{}".format(pre_parameter))
    #         logging.info("执行前置接口测试用例：{}".format(pre_test_info))
    #         code, data = apiSend.send_request(pre_test_info, pre_case_data)
    #
    #         # 检查接口是否调用成功
    #         if data:
    #             # 处理当前接口入参：获取入参-获取关联值-替换关联值
    #             parameter = read_json(case_data['summary'], case_data['parameter'], case_path)
    #             __relevance = readRelevance.get_relevance(data, parameter, __relevance)
    #             parameter = replaceRelevance.replace(parameter, __relevance)
    #             case_data['parameter'] = parameter
    #             logging.debug("请求参数处理结果：{}".format(parameter))
    #
    #             # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
    #             expected_rs = read_json(case_data['summary'], case_data['check_body']['expected_result'], case_path)
    #             parameter['data'] = data
    #             __relevance = readRelevance.get_relevance(parameter, expected_rs, __relevance)
    #             expected_rs = replaceRelevance.replace(expected_rs, __relevance)
    #             case_data['check_body']['expected_result'] = expected_rs
    #             logging.debug("期望返回处理结果：{}".format(case_data))
    #             break
    #         else:
    #             time.sleep(1)
    #             logging.error("前置接口请求失败！等待1秒后重试！")
    #     else:
    #         logging.info("前置接口请求失败！尝试三次失败！")
    #         raise Exception("获取前置接口关联数据失败！")
    # else:
    #     # 处理当前接口入参：获取入参-获取关联值-替换关联值
    #     parameter = read_json(case_data['summary'], case_data['parameter'], case_path)
    #     parameter = replaceRelevance.replace(parameter, __relevance)
    #     case_data['parameter'] = parameter
    #     logging.debug("请求参数处理结果：{}".format(parameter))
    #
    #     # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
    #     expected_rs = read_json(case_data['summary'], case_data['check_body']['expected_result'], case_path)
    #     __relevance = readRelevance.get_relevance(parameter, expected_rs, __relevance)
    #     expected_rs = replaceRelevance.replace(expected_rs, __relevance)
    #     case_data['check_body']['expected_result'] = expected_rs
    #     logging.debug("期望返回处理结果：{}".format(case_data))

    # 处理当前接口入参：获取入参-获取关联值-替换关联值
    parameter = read_json(case_data['summary'], case_data['parameter'], case_path)
    parameter = replaceRelevance.replace(parameter, __relevance)
    case_data['parameter'] = parameter
    logging.debug("请求参数处理结果：{}".format(parameter))

    # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
    expected_rs = read_json(case_data['summary'], case_data['check_body']['expected_result'], case_path)
    __relevance = readRelevance.get_relevance(parameter, expected_rs, __relevance)
    expected_rs = replaceRelevance.replace(expected_rs, __relevance)
    case_data['check_body']['expected_result'] = expected_rs
    logging.debug("期望返回处理结果：{}".format(case_data))
    return test_info, case_data


def init_flow_info(flow_info):
    """
    用例前提条件执行，组装场景用例
    :param flow_info: 场景信息-流调用流程接口用例
    :return: flow_case_data 场景用例数据
    """
    # 获取项目公共关联值
    flow_case_data = []
    aconfig = readYaml.read_yaml_data(API_CONFIG)
    for item in flow_info:
        case_path, case_describe = list(item.items())[0]
        case_dir_path, case_file_path, case_suite, case_index = case_path.split(".")
        case_file_path = PAGE_DIR + "/{}/{}.yaml".format(case_dir_path, case_file_path)
        case_data = readYaml.read_yaml_data(case_file_path)
        __relevance = aconfig[PROJECT_NAME]
        if "[" in case_index and ":" in case_index:
            case_index_right, case_index_left = case_index.strip("[").strip("]").split(":")
            case_index_right, case_index_left = int(case_index_right), int(case_index_left)
            for test_case_data in case_data.get(case_suite)[case_index_right:case_index_left]:
                test_case = {
                    "test_info": replaceRelevance.replace(case_data.get("test_info"), __relevance),
                    "test_case": test_case_data
                }
                # 处理测试信息
                logging.debug("场景测试信息处理结果：{}".format(test_case))
                flow_case_data.append(test_case)
        elif "[" in case_index:
            case_index_list = case_index.strip("[").strip("]").split(",")
            for case_index in case_index_list:
                test_case = {
                    "test_info": replaceRelevance.replace(case_data.get("test_info"), __relevance),
                    "test_case": case_data.get(case_suite)[int(case_index)]
                }
                # 处理测试信息
                logging.debug("场景测试信息处理结果：{}".format(test_case))
                flow_case_data.append(test_case)

        else:
            test_case = {
                "test_info": replaceRelevance.replace(case_data.get("test_info"), __relevance),
                "test_case": case_data.get(case_suite)[int(case_index)]
            }
            # 处理测试信息
            logging.debug("场景测试信息处理结果：{}".format(test_case))
            flow_case_data.append(test_case)
    return flow_case_data
