import copy
import importlib

import jsonpath
from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse


def jsonpath_replace(json_object, json_path, new_value):
    json_path_expr = parse(json_path)
    for match in json_path_expr.find(json_object):
        path = match.path  # 这是获取到匹配结果的路径
        if isinstance(path, Index):
            match.context.value[match.path.index] = new_value
        elif isinstance(path, Fields):
            match.context.value[match.path.fields[0]] = new_value
    return json_object


def jsonpath_find(json_object, json_path):
    value = jsonpath.jsonpath(json_object, json_path)
    return value


def deal_response_info(cache, test_info, test_case, data, responses):
    try:
        data_map = {
            "test_info": test_info,
            "test_case": test_case,
            "response_body": data
        }
        all_items = test_case.get('set_cache', {})
        if not all_items:
            all_items = {}
        for cache_key, data_path in all_items.items():
            data_type, json_path = data_path.strip().split(":")
            if "[all]" in json_path:
                json_path = json_path.replace("[all]", "")
                cache_value = jsonpath_find(data_map.get(data_type, {}), json_path)
            else:
                cache_value = jsonpath_find(data_map.get(data_type, {}), json_path)[0]
            cache.set(cache_key, cache_value)
    except Exception as error:
        print("设置cache异常:{}，跳过此操作".format(error))
    try:
        if test_case.get("script", ""):
            Script = importlib.import_module("project.script.{}".format(test_case.get("script")))
            Script_func = dir(Script)
            if "after_run" in Script_func:
                Script.after_run(cache, test_info, test_case, data, responses)
    except Exception as error:
        if "Check Error" in str(error):
            raise error
        else:
            print("执行后置处理脚本异常:{}，跳过此操作".format(error))


def deal_request_info(cache, test_info, test_case):
    test_info = copy.deepcopy(test_info)
    try:
        data_map = {
            "test_info": test_info,
            "test_case": test_case
        }
        all_items = test_case.get('replace_cache', {})
        if not all_items:
            all_items = {}
        for data_path, cache_key in all_items.items():
            if ":" in cache_key:
                value_type, value = cache_key.split(":")
                if value_type:
                    type_map = {
                        "integer": int,
                        "float": float,
                        "string": str,
                        "array": list,
                        "object": eval,
                        "boolean": bool
                    }
                    new_value = type_map.get(value_type)(value)
                else:
                    new_value = cache_key
            else:
                new_value = cache.get(cache_key, "")
            data_type, json_path = data_path.strip().split(":")
            jsonpath_replace(data_map.get(data_type, {}), json_path, new_value)
    except Exception as error:
        print("处理cache异常:{}，跳过此操作".format(error))
    try:
        if test_case.get("script", ""):
            Script = importlib.import_module("project.script.{}".format(test_case.get("script")))
            Script_func = dir(Script)
            if "before_run" in Script_func:
                test_info, test_case = Script.before_run(cache, test_info, test_case)
    except Exception as error:
        print("执行前置脚本异常:{}，跳过此操作".format(error))
    return test_info, test_case

# test_info:json_path
# test_case:json_path
# response_body:json_path
# json_path:cache
