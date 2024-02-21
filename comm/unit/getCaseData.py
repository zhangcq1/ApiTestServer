# -*- coding:utf-8 -*-
import os

import allure
import pytest
from comm.utils.readYaml import read_yaml_data
from config import FLOW_DIR, PAGE_DIR, API_CONFIG, TEST_MARKERS


def get_all_yaml(dir_path, yaml_file_path_list=None):
    if yaml_file_path_list is None:
        yaml_file_path_list = set()
    # path_list = os.listdir(dir_path)
    # for unknown_path_name in path_list:
    # unknown_path = dir_path + "/" + unknown_path_name
    if os.path.isdir(dir_path):
        for unknown_path_name in os.listdir(dir_path):
            unknown_path = dir_path + "/" + unknown_path_name
            get_all_yaml(unknown_path, yaml_file_path_list)
    elif ".yaml" in dir_path:
        yaml_file_path_list.add(dir_path)
    else:
        pass
    return yaml_file_path_list


def get_other_flow_data(dir_path=FLOW_DIR):
    """
    :param dir_path: yaml文件地址
    :return:
    """
    flow_data_list = []
    if type(dir_path) == str:
        yaml_file_path_list = get_all_yaml(dir_path)
    else:
        yaml_file_path_list = PAGE_DIR
    for yaml_file_path in yaml_file_path_list:
        yaml_file_data = read_yaml_data(yaml_file_path)
        flow_data_list.append(yaml_file_data)
    return flow_data_list


def get_flow_data(dir_path=FLOW_DIR):
    """
    :param dir_path: yaml文件地址
    :return:
    """
    if type(dir_path) == str:
        yaml_file_path_list = get_all_yaml(dir_path)
    else:
        yaml_file_path_list = PAGE_DIR
    for yaml_file_path in yaml_file_path_list:
        yaml_file_data = read_yaml_data(yaml_file_path)
        marks = []
        markers = yaml_file_data.get("markers", [])
        if not markers:
            markers = []
        for marker in markers:
            if TEST_MARKERS.get(marker):
                marks.append(TEST_MARKERS.get(marker))
        marks.extend([
            allure.story(yaml_file_data.get("case_name"))
        ])
        yield pytest.param(yaml_file_data, marks=marks)


def get_all_case_data(dir_path=PAGE_DIR):
    """
    :param dir_path: yaml文件地址
    :return:
    """
    api_conf = read_yaml_data(API_CONFIG)
    route_type = api_conf.get("project").get("route_type")
    if type(dir_path) == str:
        yaml_file_path_list = get_all_yaml(dir_path)
    else:
        yaml_file_path_list = PAGE_DIR
    for yaml_file_path in yaml_file_path_list:
        yaml_file_data = read_yaml_data(yaml_file_path)
        test_info = yaml_file_data.get("test_info")
        if route_type == "new":
            if "address_" in test_info.keys():
                test_info["address"] = test_info.get("address_")
            else:
                test_info["address"] = test_info.get("address_saas")
        test_info["yaml_file_path"] = yaml_file_path
        del yaml_file_data["test_info"]
        for case_suite_name, case_list in yaml_file_data.items():
            for one_case in case_list:
                case_data = {
                    "test_info": test_info,
                    "test_case": one_case
                }
                marks = []
                if one_case.get("markers", []):
                    markers = one_case.get("markers", [])
                else:
                    markers = []
                for marker in markers:
                    if TEST_MARKERS.get(marker):
                        marks.append(TEST_MARKERS.get(marker))
                marks.extend([
                    # allure.feature(test_info.get("address").split("}")[-1]),
                    pytest.mark.run(order=one_case.get("order")),
                    allure.story(one_case.get("summary"))
                ])
                yield pytest.param(case_data, marks=marks)

# if __name__ == '__main__':
#     case_path = FLOW_DIR + "/demo"
#     all_case_data = get_flow_data(case_path)
