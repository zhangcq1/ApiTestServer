# -*- coding:utf-8 -*-
import hashlib
import re
import warnings

import requests

from config import *

warnings.filterwarnings('ignore')


def sha256(admin_pwd):
    hash = hashlib.sha256()
    hash.update(bytes(admin_pwd, encoding='utf-8'))
    return hash.hexdigest()


def get_login_headers(host, admin_user, admin_pwd, fe_port):
    lookup_url = "https://{}:{}/api/lookup?language=zh-CN&os=web".format(host, fe_port)
    login_url = "https://{}:{}/api/demo?language=zh-CN&os=web".format(host, fe_port)
    data = {
        "user_name": admin_user,
        "password": sha256(admin_pwd),
        "platform": ""
    }
    session = requests.Session()
    lookup_response = session.post(url=lookup_url, json=data, verify=False)
    session.cookies.update(lookup_response.cookies)
    login_response = session.post(url=login_url, json=data, verify=False)
    session.cookies.update(login_response.cookies)
    session.headers["csrf-token"] = re.findall("csrf-token=(.*?) ", str(session.cookies))[0]
    cookie = "; ".join(["{}={}".format(item[0], item[1]) for item in session.cookies.items()])
    csrf_token = session.headers["csrf-token"]
    headers = {
        "cookie": cookie,
        "csrf-token": csrf_token
    }
    return headers


def update_info(version, host, headers, fe_port, admin_port):
    info_me_url = "https://{}:{}/api/info/me?language=zh-CN&os=web".format(host, fe_port)
    info_me = requests.get(url=info_me_url, headers=headers, verify=False).json()
    admin_domain = info_me.get("data", {}).get('admin_domain', "")
    admin_port_ = admin_domain.split(":")[-1]
    if admin_port == 8443:
        if "." in admin_port_:
            admin_port = 443
        else:
            admin_port = admin_port_
    print(host, version, fe_port, admin_port)
    return version, fe_port, admin_port


def write_config(conf):
    print("运行配置：{}".format(conf))
    _host = conf.get("domain", "")
    config_content = ""
    default_conf = {
        "version": "v2099",
        "run_type": "test",
        "fe_port": "443",
        "admin_port": "8443",
        "admin_user": "admin@feilian.local",
        "admin_pwd": "admin=corplink2020!"
    }
    info = DMC.get(_host, None)
    print(info)
    if info:
        for key, value in info.items():
            conf[key] = value
    else:
        for key, value in conf.items():
            if not value and key in default_conf.keys():
                conf[key] = default_conf[key]
        for key, value in default_conf.items():
            if key in default_conf.keys() and key not in conf.keys():
                conf[key] = value
    headers = get_login_headers(_host, conf["admin_user"], conf["admin_pwd"], conf["fe_port"])
    conf["version"], conf["fe_port"], conf["admin_port"] = \
        update_info(conf["version"], _host, headers, conf["fe_port"], conf["admin_port"])
    cookie = headers.get("cookie")
    csrf_token = headers.get("csrf-token")
    print(info)
    with open(API_CONFIG, "r", encoding="utf8") as config_file_obj:
        for line in config_file_obj:
            if "host:" in line:
                line = line.split(":")[0] + ": {}\n".format(_host)
            if "cookie:" in line:
                line = line.split(":")[0] + ": {}\n".format(cookie)
            if "csrf-token:" in line:
                line = line.split(":")[0] + ": {}\n".format(csrf_token)
            if "route_type:" in line:
                if conf["version"] == "saas" or conf["version"] == "private":
                    line = line.split(":")[0] + ": {}\n".format('new')
                else:
                    line = line.split(":")[0] + ": {}\n".format('old')
            if "fe_port:" in line:
                line = line.split(":")[0] + ": {}\n".format(conf.get("fe_port", conf["fe_port"]))
            if "admin_port:" in line:
                line = line.split(":")[0] + ": {}\n".format(conf.get("admin_port", conf["admin_port"]))
            if "other:" in line:
                if info and info.get("other"):
                    line = line.split(":")[0] + ": {}\n".format(info.get("other"))
                else:
                    line = line.split(":")[0] + ": \n"
            config_content += line
    with open(API_CONFIG, "w", encoding="utf8") as config_file_obj:
        config_file_obj.write(config_content)
    return conf["version"]
