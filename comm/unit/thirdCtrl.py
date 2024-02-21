import datetime
import hashlib
import random

import requests

from comm.utils.readYaml import read_yaml_data, write_yaml_file
from comm.utils.randomly import generate_phone, generate_now_timestamp
from config import THIRD_CONFIG


def init():
    config = read_yaml_data(THIRD_CONFIG)
    result = {}

    feishu_config = config['feishu']
    feishu = {
        'url': 'https://{}/open-apis/auth/v3/tenant_access_token/internal'.format(feishu_config['host']),
        'headers': {'Content-Type': 'application/json; charset=utf-8'},
        'body': {
            'app_id': feishu_config['app_id'],
            'app_secret': feishu_config['app_secret']
        }
    }
    feishu_res = requests.post(url=feishu['url'], headers=feishu['headers'], json=feishu['body'])
    feishu_res = feishu_res.json()
    if feishu_res['code'] == 0:
        result['code'] = 0
        result['type'] = 'feishu',
        result['token'] = feishu_res['tenant_access_token']
        config['tokens']['feishu'] = feishu_res['tenant_access_token']
        write_yaml_file(THIRD_CONFIG, config)
    else:
        result['code'] = feishu_res['code']
        result['type'] = 'feishu',
        result['message'] = feishu_res['msg']

    weixin_config = config['weixin']
    weixin = {
        'url': 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(weixin_config['app_id'],
                                                                                             weixin_config[
                                                                                                 'base_secret'])
    }
    weixin_res = requests.get(url=weixin['url'])
    weixin_res = weixin_res.json()
    if weixin_res['errcode'] == 0:
        result['code'] = 0
        result['type'] = 'weixin'
        result['token'] = weixin_res['access_token']
        config['tokens']['weixin'] = weixin_res['access_token']
        write_yaml_file(THIRD_CONFIG, config)
    else:
        result['code'] = weixin_res['errcode']
        result['type'] = 'weixin'
        result['message'] = weixin_res['errmsg']
    return result


def user(source, command, param=None):
    config = read_yaml_data(THIRD_CONFIG)

    def feishu(command, param=None):
        headers = {
            'Authorization': 'Bearer ' + config['tokens']['feishu'],
            'Content-Type': 'application/json; charset=utf-8'
        }

        def create(param=None):
            mobile = generate_phone()
            url = 'https://{}/open-apis/contact/v3/users'.format(config['feishu']['host'])
            body = {
                'name': 'apitest_{}-feishu'.format(generate_now_timestamp()),
                'mobile': mobile,
                'email': '{}@mxin.me'.format(mobile),
                'department_ids': [config['feishu']['open_department_id']],
                'employee_type': 1,
            }
            res = requests.post(url=url, headers=headers, json=body).json()
            if res['code'] == 0 and res['msg'] == 'success':
                body['user_id'] = res['data']['user']['user_id']
                body['open_id'] = res['data']['user']['open_id']
                return body
            else:
                raise ValueError('Check Error: Create User Fail: [code: {}, msg: {}]'.format(res['code'], res['msg']))

        def update(param=None):
            url = 'https://{}/open-apis/contact/v3/users/{}?user_id_type=open_id'.format(config['feishu']['host'],
                                                                                         param['open_id'])
            body = {
                'name': param['name']
            }
            res = requests.patch(url=url, headers=headers, json=body).json()
            if res['code'] == 0 and res['msg'] == 'success':
                return body
            else:
                raise ValueError('Check Error: Update User Fail: [code: {}, msg: {}]'.format(res['code'], res['msg']))

        def delete(param=None):
            url = 'https://{}/open-apis/contact/v3/users/{}?user_id_type=open_id'.format(config['feishu']['host'],
                                                                                         param['open_id'])
            res = requests.delete(url=url, headers=headers).json()
            if res['code'] == 0 and res['msg'] == 'success':
                return 'success'
            else:
                raise ValueError('Check Error: Delete User Fail: [code: {}, msg: {}]'.format(res['code'], res['msg']))

        command_map = {
            'create': create,
            'update': update,
            'delete': delete
        }
        select_command = command_map.get(command)
        if select_command:
            return select_command(param)
        else:
            raise ValueError('Check Error: Command Error')

    def dingtalk(command, param=None):
        print(456, command)
        pass

    def weixin(command, param=None):
        proxy_url = 'https://api.mxin.moe/fl/proxy/weixin'
        current_time = datetime.datetime.now().strftime("%Y%m%d%H")
        string = f"mxin{current_time}mxin".encode('utf-8')
        secret = hashlib.sha256(string).hexdigest()
        headers = {
            'secret': secret
        }

        def create(param=None):
            mobile = generate_phone()
            nowtime = generate_now_timestamp()
            data = {
                'url': 'https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token={}'.format(
                    config['tokens']['weixin']),
                'method': 'POST',
                'body': {
                    'userid': 'apitest_{}-weixin'.format(nowtime),
                    'name': 'apitest_{}-weixin'.format(nowtime),
                    'mobile': mobile,
                    'email': '{}@mxin.me'.format(mobile),
                    'department': [config['weixin']['open_department_id']]
                }
            }
            res = requests.post(url=proxy_url, headers=headers, json=data).json()
            if res['errcode'] == 0 and res['errmsg'] == 'created':
                data['body']['user_id'] = data['body'].pop('userid')
                return data['body']
            else:
                raise ValueError(
                    'Check Error: Create User Fail: [code: {}, msg: {}]'.format(res['errcode'], res['errmsg']))

        def update(param=None):
            data = {
                'url': 'https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token={}'.format(
                    config['tokens']['weixin']),
                'method': 'POST',
                'body': {
                    'userid': param['user_id'],
                    'name': param['name']
                }
            }
            res = requests.post(url=proxy_url, headers=headers, json=data).json()
            if res['errcode'] == 0 and res['errmsg'] == 'updated':
                data['body']['user_id'] = data['body'].pop('userid')
                return data['body']
            else:
                raise ValueError(
                    'Check Error: Update User Fail: [code: {}, msg: {}]'.format(res['errcode'], res['errmsg']))

        def delete(param=None):
            data = {
                'url': 'https://qyapi.weixin.qq.com/cgi-bin/user/delete?access_token={}&userid={}'.format(
                    config['tokens']['weixin'], param['user_id']),
                'method': 'GET',
                'body': {}
            }
            res = requests.post(url=proxy_url, headers=headers, json=data).json()
            if res['errcode'] == 0 and res['errmsg'] == 'deleted':
                return 'success'
            else:
                raise ValueError(
                    'Check Error: Delete User Fail: [code: {}, msg: {}]'.format(res['errcode'], res['errmsg']))

        command_map = {
            'create': create,
            'update': update,
            'delete': delete
        }
        select_command = command_map.get(command)
        if select_command:
            return select_command(param)
        else:
            raise ValueError('Check Error: Command Error')

    source_map = {
        'feishu': feishu,
        'weixin': weixin,
        'dingtalk': dingtalk
    }
    select_source = source_map.get(source)
    if select_source:
        return select_source(command, param)
    else:
        raise ValueError('Check Error: Source Error')
