import hashlib
import json
import random
import time
import xlwings as xw


class userData(object):
    def feishuData(self, department_ids=None, email=None, mobile=None, name=None, userId=None):
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open('/Users/bytedance/Downloads/topgo1.xlsx')
        sheet = wb.sheets[0]
        # for userId in sheet:
        A = 'A{}'.format(random.randint(4, 50))
        print(A)
        print(sheet[A].value)


# data = userData()
# data.feishuData()


class feiShu(object):
    def __init__(self, app_id='cli_a297072c5978900e', token='JTL81aPHxB2QwHWdVA1Z7fqAbHnrg6fF'):
        self.app_id = app_id
        self.token = token

    def contact_user_created_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'event_type': 'contact.user.created_v3',
                'create_time': '{}'.format(str(round(t * 1000))),
                'token': '{}'.format(self.token),
                'app_id': '{}'.format(self.app_id),
                'tenant_key': '2ca1d211f64f6438'
            },
            'event': {
                'object': {
                    'avatar': {
                        'avatar_240': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_3adbb5a2-5b6b-456e-bf2e-58dc6621c78g~?image_size=240x240&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_640': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_3adbb5a2-5b6b-456e-bf2e-58dc6621c78g~?image_size=640x640&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_72': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_3adbb5a2-5b6b-456e-bf2e-58dc6621c78g~?image_size=72x72&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_origin': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_3adbb5a2-5b6b-456e-bf2e-58dc6621c78g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp'
                    },
                    'city': '',
                    'country': '',
                    'department_ids': [
                        '0'
                    ],  # true
                    'employee_no': '',
                    'employee_type': 1,
                    'en_name': '',
                    'enterprise_email': '',  # true
                    'gender': 0,
                    'job_title': '',
                    'join_time': 1689120000,
                    'mobile': '+8617600130712',  # true
                    'name': '测011',  # true
                    'nickname': '',
                    'open_id': 'ou_8593d145657483ae2414b72798bf5d26',
                    'orders': [
                        {
                            'department_id': '0',
                            'department_order': 1,
                            'is_primary_dept': True,
                            'user_order': 0
                        }
                    ],
                    'status': {
                        'is_activated': False,
                        'is_exited': False,
                        'is_frozen': False,
                        'is_resigned': False,
                        'is_unjoin': True
                    },
                    'union_id': 'on_a78474520390b51035fa40636e0d3ee3',
                    'user_id': 'db7feg37',  # true
                    'work_station': ''
                },
                'old_object': {
                    'avatar': {
                        'avatar_240': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_430bf382-fff4-4e25-92f1-0a1b2051e5cg~?image_size=240x240&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_640': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_430bf382-fff4-4e25-92f1-0a1b2051e5cg~?image_size=640x640&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_72': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_430bf382-fff4-4e25-92f1-0a1b2051e5cg~?image_size=72x72&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_origin': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_430bf382-fff4-4e25-92f1-0a1b2051e5cg~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp'
                    },
                    'name': '测01',  # true
                    'open_id': 'ou_8593d145657483ae2414b72798bf5d26',
                    'union_id': 'on_a78474520390b51035fa40636e0d3ee3'
                }
            }
        }
        return json.dumps(schema)

    def contact_user_deleted_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'token': '{}'.format(self.token),
                'create_time': '{}'.format(str(round(t * 1000))),
                'event_type': 'contact.user.deleted_v3',
                'tenant_key': '2ddff0f7544fd75e',
                'app_id': '{}'.format(self.app_id),
            },
            'event': {
                'object': {
                    'avatar': {
                        'avatar_240': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_80df4836-95b6-40cc-94c8-cd869b28186g~?image_size=240x240&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_640': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_80df4836-95b6-40cc-94c8-cd869b28186g~?image_size=640x640&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_72': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_80df4836-95b6-40cc-94c8-cd869b28186g~?image_size=72x72&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_origin': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_80df4836-95b6-40cc-94c8-cd869b28186g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp'
                    },
                    'city': '',
                    'country': '',
                    'employee_no': '',
                    'employee_type': 1,
                    'en_name': '',
                    'enterprise_email': '',
                    'gender': 0,
                    'job_title': '',
                    'join_time': 1683648000,
                    'mobile': '+8618005109001',
                    'name': '0510cccc09',
                    'nickname': '',
                    'open_id': 'ou_e6d02d5fab79b71aa323eea01f786f3a',
                    'status': {
                        'is_activated': False,
                        'is_exited': False,
                        'is_frozen': False,
                        'is_resigned': True,
                        'is_unjoin': True
                    },
                    'union_id': 'on_35288d614d4a1164c21670d0da4dc492',
                    'user_id': 'e1f564e1',
                    'work_station': ''
                },
                'old_object': {
                    'department_ids': [
                        'od-51d6cb3a6e1589a35a6f30307d09e7d1'
                    ],
                    'open_id': 'ou_e6d02d5fab79b71aa323eea01f786f3a'
                }
            }
        }
        return json.dumps(schema)

    def contact_user_updated_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'token': '{}'.format(self.token),
                'create_time': '{}'.format(str(round(t * 1000))),
                'event_type': 'contact.user.updated_v3',
                'tenant_key': '2ddff0f7544fd75e',
                'app_id': '{}'.format(self.app_id),
            },
            'event': {
                'object': {
                    'avatar': {
                        'avatar_240': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_e87c73a8-7bf0-4c38-a88c-460e9f9236fg~?image_size=240x240&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_640': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_e87c73a8-7bf0-4c38-a88c-460e9f9236fg~?image_size=640x640&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_72': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_e87c73a8-7bf0-4c38-a88c-460e9f9236fg~?image_size=72x72&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_origin': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_e87c73a8-7bf0-4c38-a88c-460e9f9236fg~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp'
                    },
                    'city': '',
                    'country': '',
                    'department_ids': [
                        '0'
                    ],
                    'employee_no': '',
                    'employee_type': 1,
                    'en_name': '',
                    'enterprise_email': '',
                    'gender': 0,
                    'job_title': '',
                    'join_time': 1689120000,
                    'mobile': '+8617600150712',
                    'name': '测试07121asd33',
                    'nickname': '',
                    'open_id': 'ou_916100285c96d14177c66c5b1773852d',
                    'orders': [
                        {
                            'department_id': '0',
                            'department_order': 1,
                            'is_primary_dept': True,
                            'user_order': 0
                        }
                    ],
                    'status': {
                        'is_activated': False,
                        'is_exited': False,
                        'is_frozen': False,
                        'is_resigned': False,
                        'is_unjoin': True
                    },
                    'union_id': 'on_aed722fda7f95dd963f115e929a2c589',
                    'user_id': 'd138f1c4',
                    'work_station': ''
                },
                'old_object': {
                    'avatar': {
                        'avatar_240': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_f74e2bd7-f770-4417-b794-2514b1866b2g~?image_size=240x240&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_640': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_f74e2bd7-f770-4417-b794-2514b1866b2g~?image_size=640x640&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_72': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_f74e2bd7-f770-4417-b794-2514b1866b2g~?image_size=72x72&cut_type=&quality=&format=png&sticker_format=.webp',
                        'avatar_origin': 'https://s1-imfile.feishucdn.com/static-resource/v1/v2_f74e2bd7-f770-4417-b794-2514b1866b2g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp'
                    },
                    'name': '测试07121asd',
                    'open_id': 'ou_916100285c96d14177c66c5b1773852d',
                    'union_id': 'on_aed722fda7f95dd963f115e929a2c589'
                }
            }
        }
        return json.dumps(schema)

    def contact_department_created_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'token': '{}'.format(self.token),
                'create_time': '{}'.format(str(round(t * 1000))),
                'event_type': 'contact.department.created_v3',
                'tenant_key': '2ddff0f7544fd75e',
                'app_id': '{}'.format(self.app_id),
            },
            'event': {
                'object': {
                    'department_id': 'f95ga4g83fedb757',
                    'name': 'testzeng',
                    'open_department_id': 'od-45dcfd8a9287905e5f25a9e9bca2101f',
                    'order': 2000,
                    'parent_department_id': 'od-eb30617974c4d92297f9c647f3bbe404',
                    'status': {
                        'is_deleted': False
                    }
                }
            }
        }

        return json.dumps(schema)

    def contact_department_updated_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'token': '{}'.format(self.token),
                'create_time': '{}'.format(str(round(t * 1000))),
                'event_type': 'contact.department.updated_v3',
                'tenant_key': '2ddff0f7544fd75e',
                'app_id': '{}'.format(self.app_id),
            },
            'event': {
                'object': {
                    'chat_id': 'oc_f2123effd3afdf0715693be74f3f7afb',
                    'department_id': 'f95ga4g83fedb757',
                    'name': 'testzeng',
                    'open_department_id': 'od-45dcfd8a9287905e5f25a9e9bca2101f',
                    'order': 2000,
                    'parent_department_id': 'od-eb30617974c4d92297f9c647f3bbe404',
                    'status': {
                        'is_deleted': False
                    }
                },
                'old_object': [

                ]
            }
        }
        return json.dumps(schema)

    def contact_department_deleted_v3(self):
        t = time.time()
        m = hashlib.md5()
        m.update(str(round(t * 1000)).encode('utf8'))
        m = m.hexdigest()
        schema = {
            'schema': '2.0',
            'header': {
                'event_id': '{}'.format(m),
                'token': '{}'.format(self.token),
                'create_time': '{}'.format(str(round(t * 1000))),
                'event_type': 'contact.department.deleted_v3',
                'tenant_key': '2ddff0f7544fd75e',
                'app_id': '{}'.format(self.app_id),
            },
            'event': {
                'object': {
                    'department_id': 'f95ga4g83fedb757',
                    'name': 'testzeb',
                    'open_department_id': 'od-07cccd0fe678b7c97ab331ec7deea121',
                    'order': 4000,
                    'parent_department_id': 'od-eb30617974c4d92297f9c647f3bbe404',
                    'status': {
                        'is_deleted': True
                    }
                },
                'old_object': {
                    'open_department_id': 'od-07cccd0fe678b7c97ab331ec7deea121',
                    'status': {
                        'is_deleted': True
                    }
                }
            }
        }
        return json.dumps(schema)

# t = feiShu()
# print(t.contact_user_created_v3())
