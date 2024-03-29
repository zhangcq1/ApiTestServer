# -*- coding:utf-8 -*-
import re

from config import *

pattern_var = r"\${(.*?)}"
pattern_eval = r"\$Eval\((.*?)\)"


def replace_cache(value, relevance):
    """优先处理缓存信息

    :param value: 原始值
    :param relevance : 关联对象
    :return:
    """
    if isinstance(value, str) and relevance:
        cache = relevance.get("cache")
        if "${" in value and cache:
            result = re.findall(pattern_var, value)
            for item in result:
                new_item = cache.get(item, None)
                if new_item:
                    value = value.replace("${%s}" % (item), str(new_item))
    return value


def replace_pattern(pattern, value):
    """替换正则表达式

    :param pattern: 匹配字符
    :param value: 匹配值
    :return:
    """
    patterns = pattern.split('(.*?)')
    return ''.join([patterns[0], value, patterns[-1]])


def replace_relevance(param, relevance=None):
    """替换变量关联值

    :param param: 参数对象
    :param relevance: 关联对象
    :return:
    """
    result = re.findall(pattern_var, str(param))
    if (not result) or (not relevance):
        pass
    else:
        for each in result:
            try:
                # 关联值只考虑一个值
                # value = relevance[each]
                # pattern = re.compile(r'\${' + each + '}')
                # try:
                # 	param = re.sub(pattern, value, param)
                # except TypeError:
                # 	param = value

                # 关联参数多值时一一对应替换
                # relevance_index = 0
                # if isinstance(relevance[each], list):
                # 	try:
                # 		param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
                # 		relevance_index += 1
                # 	except IndexError:
                # 		relevance_index = 0
                # 		param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
                # 		relevance_index += 1

                # 关联参数多值时指定索引值替换
                mark = re.findall(r"\[\-?[0-9]*\]", each)
                # 判断关联参数是否指定索引值var[n]
                if len(mark) == 0:
                    if isinstance(relevance[each], list):
                        value = relevance[each][0]
                    else:
                        value = relevance[each]
                elif len(mark) == 1:
                    var = each.strip(mark[0])
                    n = int(mark[0].strip('[').strip(']'))
                    value = relevance[var][n]
                    each = each.replace('[', '\[').replace(']', '\]')
                else:
                    var = each
                    for m in mark:
                        var = var.replace(m, '')
                    n1 = int(mark[0].strip('[').strip(']'))
                    n2 = int(mark[1].strip('[').strip(']'))
                    value = relevance[var][n1][n2]
                    each = each.replace('[', '\[').replace(']', '\]')

                # 生成正在表达式并替换关联参数
                pattern = re.compile('\${' + each + '}')
                try:
                    if param.strip('${' + each + '}'):
                        param = re.sub(pattern, str(value), param)
                    else:
                        param = re.sub(pattern, value, param)
                except TypeError:
                    param = value
            except KeyError:
                pass
                # raise KeyError('替换变量{0}失败，未发现变量对应关联值！\n关联列表：{1}'.format(param, relevance))
            # pass
    return param


def replace_eval(param):
    """替换eval表达式结果

    :param param: 参数对象
    :return:
    """
    result = re.findall(pattern_eval, str(param))
    if not result:
        pass
    else:
        for each in result:
            try:
                if 'import' in each:
                    raise Exception('存在非法标识import')
                else:
                    value = str(eval(each))
                    param = re.sub(pattern_eval, value, param)
            except KeyError as e:
                raise Exception('获取值[ % ]失败！\n%'.format(param, e))
            except SyntaxError:
                pass
    return param


def replace_random(param):
    """替换随机方法参数值

    :param param:
    :return:
    """
    for gen_name, gen_fun in GEN_MAP.items():
        pattern_gen = r'\${}\(\)'.format(gen_name)
        gen_list = re.findall(pattern_gen, str(param))
        if len(gen_list):
            for i in gen_list:
                param = re.sub(pattern_gen, str(gen_fun()), param, count=1)
    return param


def replace(param, relevance=None):
    """替换参数对应关联数据

    :param param: 参数对象
    :param relevance: 关联对象
    :return:
    """
    if not param:
        pass
    elif isinstance(param, dict):
        deal_keys = {}
        for key, value in param.items():
            if "${" in key:
                new_key = replace_cache(key, relevance)
                deal_keys[key] = new_key
            if isinstance(value, dict):
                param[key] = replace(value, relevance)
            elif isinstance(value, list):
                for index, sub_value in enumerate(value):
                    param[key][index] = replace(sub_value, relevance)
            else:
                value = replace_cache(value, relevance)
                value = replace_relevance(value, relevance)
                value = replace_random(value)
                value = replace_eval(value)
                param[key] = value
        for old_key, new_key in deal_keys.items():
            value = param.get(old_key)
            del param[old_key]
            param[new_key] = value
    elif isinstance(param, list):
        for index, value in enumerate(param):
            param[index] = replace(value, relevance)

    else:
        param = replace_cache(param, relevance)
        param = replace_relevance(param, relevance)
        param = replace_random(param)
        param = replace_eval(param)
    return param


if __name__ == '__main__':
    print('替换变量并计算表达式：', replace('$Eval(${unitCode}*1000+1)', {'unitCode': 9876543210}))
    print('生成1-9之间的随机数：', replace('$RandInt(1,9)'))
    print('生成10位随机字符：', replace('$RandStr(10)'))
    print('从列表中随机选择：', replace('$RandChoice(a,b,c,d)'))
    print('生成一个伪手机号：', replace('$GenPhone()'))
    print('生成一个guid：', replace('$GenGuid()'))
    print('生成一个伪微信ID：', replace('$GenWxid()'))
    print('生成一个伪身份证：', replace('$GenNoid()'))
    print('生成一个18岁伪身份证：', replace("$GenNoid(y-18)"))
    print('生成下个月今天的日期：', replace("$GenDate(m+1)"))
    print('生成昨天此时的时间：', replace("$GenDatetime(d-1)"))
    print('通过索引指定关联值：', replace('${name[-1]}', {'name': ['test1', 'test2']}))
    print('生成一个伪邮箱：', replace('$GenEmail()'))
