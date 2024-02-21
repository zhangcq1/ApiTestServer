# -*- coding:utf-8 -*-
import yaml


def read_yaml_data(yaml_file):
    """读取yaml文件数据

    :param yaml_file: yaml文件地址
    :return:
    """
    import yaml
    with open(yaml_file, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.SafeLoader)


def write_yaml_file(yaml_file, obj):
    """把对象obj写入yaml文件

    :param yaml_file: yaml文件地址
    :param obj: 数据对象
    :return:
    """
    with open(yaml_file, 'w', encoding='utf-8') as file:
        yaml.dump(obj, file, allow_unicode=True, sort_keys=False)
