# -*- coding:utf-8 -*-*
import hashlib
import re
import requests
import warnings
from comm.utils.randomly import *
from config import API_CONFIG

warnings.filterwarnings('ignore')
from comm.utils.readYaml import read_yaml_data

run_conf = read_yaml_data(API_CONFIG)
host = run_conf.get("project").get("host")
fe_port = run_conf.get("project").get("fe_port")
admin_port = run_conf.get("project").get("admin_port")
admin_headers = run_conf.get("project").get("headers")


def sha256(admin_pwd):
    hash = hashlib.sha256()
    hash.update(bytes(admin_pwd, encoding='utf-8'))
    return hash.hexdigest()


def get_user_start_password(user_id):
    params = {
        "language": "zh-CN",
        "os": "web",
        "user_id": user_id
    }
    get_user_info_url = "https://{}:{}/api/admin/v2/user/info".format(host, admin_port)
    response = requests.get(url=get_user_info_url, params=params, headers=admin_headers).json()
    login_user_start_password = response.get("data").get("start_password")
    return login_user_start_password


def get_device_report_info(os):
    mac_report_info = {
        "memory_total": 32768,
        "memory_available": 7715,
        "disk_total": 476802,
        "disk_available": 175128,
        "cpu_arch": 5,
        "cpu_model": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
        "gpu_model": "Intel UHD Graphics 630",
        "nic_type": "Wi-Fi  (0x14E4, 0x7BF)",
        "mac_addrs": [
            "3a:5e:f9:a7:2e:14",
            "16:7d:da:01:54:64",
            "16:7d:da:01:54:65",
            "82:46:e2:00:98:01",
            "82:46:e2:00:98:00",
            "82:46:e2:00:98:05",
            "ac:de:48:00:11:22",
            "fa:9c:2a:3f:3d:61",
            "ae:d4:64:87:55:57",
            "14:7d:da:10:a2:7e",
            "82:46:e2:00:98:04"
        ],
        "login_user": "bytedance",
        "is_vm": False,
        "serial_number": "C02D70MFMD6R",
        "licensed_windows": False,
        "nic_detail_list": [
            {
                "nic_type": "en2",
                "mac_addr": "82:46:e2:00:98:00",
                "active": False,
                "description": "en2",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en4",
                "mac_addr": "82:46:e2:00:98:04",
                "active": False,
                "description": "en4",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "llw0",
                "mac_addr": "fa:9c:2a:3f:3d:61",
                "active": False,
                "description": "llw0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::f89c:2aff:fe3f:3d61"
                ]
            },
            {
                "nic_type": "vmenet0",
                "mac_addr": "3a:5e:f9:a7:2e:14",
                "active": True,
                "description": "vmenet0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en0",
                "mac_addr": "14:7d:da:10:a2:7e",
                "active": True,
                "description": "en0",
                "is_virtual": False,
                "ipv4": "10.79.239.1",
                "ipv6": [
                    "fe80::c9b:257e:23fc:7482",
                    "fdbd:ff1:ce00:2c8:1c5e:18b3:abf3:7c91",
                    "fdbd:ff1:ce00:2c8::11d5"
                ]
            },
            {
                "nic_type": "en1",
                "mac_addr": "82:46:e2:00:98:01",
                "active": False,
                "description": "en1",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "bridge100",
                "mac_addr": "16:7d:da:01:54:64",
                "active": True,
                "description": "bridge100",
                "is_virtual": True,
                "ipv4": "10.211.55.2",
                "ipv6": [
                    "fe80::147d:daff:fe01:5464"
                ]
            },
            {
                "nic_type": "bridge101",
                "mac_addr": "16:7d:da:01:54:65",
                "active": True,
                "description": "bridge101",
                "is_virtual": True,
                "ipv4": "10.37.129.2",
                "ipv6": [
                    "fe80::147d:daff:fe01:5465"
                ]
            },
            {
                "nic_type": "en3",
                "mac_addr": "82:46:e2:00:98:05",
                "active": False,
                "description": "en3",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en5",
                "mac_addr": "ac:de:48:00:11:22",
                "active": True,
                "description": "en5",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::aede:48ff:fe00:1122"
                ]
            },
            {
                "nic_type": "vmenet1",
                "mac_addr": "ae:d4:64:87:55:57",
                "active": True,
                "description": "vmenet1",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "awdl0",
                "mac_addr": "fa:9c:2a:3f:3d:61",
                "active": True,
                "description": "awdl0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::f89c:2aff:fe3f:3d61"
                ]
            },
            {
                "nic_type": "bridge0",
                "mac_addr": "82:46:e2:00:98:01",
                "active": False,
                "description": "bridge0",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": []
            }
        ],
        "hdd_serial_numbers": None,
        "ssd_serial_numbers": [
            "C02031600C6NGJ21V"
        ],
        "cpu_serial_number": "",
        "mem_serial_numbers": [
            "-",
            "-"
        ],
        "windows_ad_domain_name": "",
        "windows_ad_domain_account": "",
        "joined_ad_domain": False,
        "mac_lack_full_disk_access": False,
        "mac_lack_screenshot_access": False,
        "os_install_date": 1695697912,
        "mac_mdm_profile_installed": True
    }
    windows_report_info = {
        "memory_total": 32768,
        "memory_available": 7715,
        "disk_total": 476802,
        "disk_available": 175128,
        "cpu_arch": 5,
        "cpu_model": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
        "gpu_model": "Intel UHD Graphics 630",
        "nic_type": "Wi-Fi  (0x14E4, 0x7BF)",
        "mac_addrs": [
            "3a:5e:f9:a7:2e:14",
            "16:7d:da:01:54:64",
            "16:7d:da:01:54:65",
            "82:46:e2:00:98:01",
            "82:46:e2:00:98:00",
            "82:46:e2:00:98:05",
            "ac:de:48:00:11:22",
            "fa:9c:2a:3f:3d:61",
            "ae:d4:64:87:55:57",
            "14:7d:da:10:a2:7e",
            "82:46:e2:00:98:04"
        ],
        "login_user": "bytedance",
        "is_vm": False,
        "serial_number": "C02D70MFMD6R",
        "licensed_windows": False,
        "nic_detail_list": [
            {
                "nic_type": "bridge100",
                "mac_addr": "16:7d:da:01:54:64",
                "active": True,
                "description": "bridge100",
                "is_virtual": True,
                "ipv4": "10.211.55.2",
                "ipv6": [
                    "fe80::147d:daff:fe01:5464"
                ]
            },
            {
                "nic_type": "bridge101",
                "mac_addr": "16:7d:da:01:54:65",
                "active": True,
                "description": "bridge101",
                "is_virtual": True,
                "ipv4": "10.37.129.2",
                "ipv6": [
                    "fe80::147d:daff:fe01:5465"
                ]
            },
            {
                "nic_type": "en1",
                "mac_addr": "82:46:e2:00:98:01",
                "active": False,
                "description": "en1",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en2",
                "mac_addr": "82:46:e2:00:98:00",
                "active": False,
                "description": "en2",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "vmenet0",
                "mac_addr": "3a:5e:f9:a7:2e:14",
                "active": True,
                "description": "vmenet0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "vmenet1",
                "mac_addr": "ae:d4:64:87:55:57",
                "active": True,
                "description": "vmenet1",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "awdl0",
                "mac_addr": "fa:9c:2a:3f:3d:61",
                "active": True,
                "description": "awdl0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::f89c:2aff:fe3f:3d61"
                ]
            },
            {
                "nic_type": "en0",
                "mac_addr": "14:7d:da:10:a2:7e",
                "active": True,
                "description": "en0",
                "is_virtual": False,
                "ipv4": "10.79.239.1",
                "ipv6": [
                    "fe80::c9b:257e:23fc:7482",
                    "fdbd:ff1:ce00:2c8:1c5e:18b3:abf3:7c91",
                    "fdbd:ff1:ce00:2c8::11d5"
                ]
            },
            {
                "nic_type": "en3",
                "mac_addr": "82:46:e2:00:98:05",
                "active": False,
                "description": "en3",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en4",
                "mac_addr": "82:46:e2:00:98:04",
                "active": False,
                "description": "en4",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": []
            },
            {
                "nic_type": "en5",
                "mac_addr": "ac:de:48:00:11:22",
                "active": True,
                "description": "en5",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::aede:48ff:fe00:1122"
                ]
            },
            {
                "nic_type": "llw0",
                "mac_addr": "fa:9c:2a:3f:3d:61",
                "active": False,
                "description": "llw0",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::f89c:2aff:fe3f:3d61"
                ]
            },
            {
                "nic_type": "bridge0",
                "mac_addr": "82:46:e2:00:98:01",
                "active": False,
                "description": "bridge0",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": []
            }
        ],
        "hdd_serial_numbers": None,
        "ssd_serial_numbers": [
            "C02031600C6NGJ21V"
        ],
        "cpu_serial_number": "",
        "mem_serial_numbers": [
            "-",
            "-"
        ],
        "windows_ad_domain_name": "",
        "windows_ad_domain_account": "",
        "joined_ad_domain": False,
        "mac_lack_full_disk_access": False,
        "mac_lack_screenshot_access": False,
        "os_install_date": 1695697912,
        "mac_mdm_profile_installed": True
    }
    linux_report_info = {
        "memory_total": 15651,
        "memory_available": 9763,
        "disk_total": 238776,
        "disk_available": 13152,
        "cpu_arch": 3,
        "cpu_model": "Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz",
        "gpu_model": "Intel Corporation UHD Graphics (rev 02)",
        "nic_type": "Intel Corporation Ethernet Connection (10) I219-V",
        "mac_addrs": [
            "70:9c:d1:c7:17:94",
            "46:51:f9:1f:d8:42",
            "02:42:f8:fd:c3:0a",
            "8c:8c:aa:44:16:32"
        ],
        "login_user": "lm",
        "is_vm": False,
        "serial_number": "PF2KR4NR",
        "licensed_windows": False,
        "nic_detail_list": [
            {
                "nic_type": "enp0s31f6",
                "mac_addr": "8c:8c:aa:44:16:32",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "wlp0s20f3",
                "mac_addr": "70:9c:d1:c7:17:94",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "100.74.30.151",
                "ipv6": [
                    "fdbd:ff1:ce00:282::c7",
                    "fdbd:ff1:ce00:282:cb5a:f974:63c0:b79c",
                    "fdbd:ff1:ce00:282:b1cc:52:f44b:c8de",
                    "fe80::551b:e137:6378:1c0a"
                ]
            },
            {
                "nic_type": "br-ex",
                "mac_addr": "46:51:f9:1f:d8:42",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "10.20.20.1",
                "ipv6": [
                    "fe80::4451:f9ff:fe1f:d842"
                ]
            },
            {
                "nic_type": "docker0",
                "mac_addr": "02:42:f8:fd:c3:0a",
                "active": False,
                "description": "",
                "is_virtual": True,
                "ipv4": "172.17.0.1",
                "ipv6": None
            }
        ],
        "hdd_serial_numbers": None,
        "ssd_serial_numbers": None,
        "cpu_serial_number": "EC 06 08 00 FF FB EB BF",
        "mem_serial_numbers": None,
        "windows_ad_domain_name": "",
        "windows_ad_domain_account": "",
        "joined_ad_domain": False,
        "mac_lack_full_disk_access": None,
        "mac_lack_screenshot_access": None,
        "os_install_date": 0,
        "mac_mdm_profile_installed": None
    }
    android_report_info = {
        "memory_total": 7444,
        "memory_available": 3639,
        "disk_total": 108372,
        "disk_available": 73521,
        "cpu_arch": 0,
        "cpu_model": "SM8325",
        "gpu_model": "",
        "nic_type": "",
        "mac_addrs": [
            "02:00:00:00:00:00"
        ],
        "login_user": "",
        "is_vm": False,
        "serial_number": "unknown",
        "licensed_windows": False,
        "nic_detail_list": [
            {
                "nic_type": "dummy0",
                "mac_addr": "02:00:00:00:00:00",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::2cab:2fff:feea:5475"
                ]
            },
            {
                "nic_type": "rmnet_data0",
                "mac_addr": "02:00:00:00:00:00",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::60d5:57ff:fecf:f62d"
                ]
            },
            {
                "nic_type": "wlan0",
                "mac_addr": "02:00:00:00:00:00",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "10.79.229.208",
                "ipv6": [
                    "fe80::b0a5:d4ff:fee8:8f60",
                    "fdbd:ff1:ce00:2c8:b0a5:d4ff:fee8:8f60",
                    "fdbd:ff1:ce00:2c8:3c62:d5fb:96bc:b1d6"
                ]
            }
        ],
        "hdd_serial_numbers": None,
        "ssd_serial_numbers": None,
        "cpu_serial_number": "",
        "mem_serial_numbers": None,
        "windows_ad_domain_name": "",
        "windows_ad_domain_account": "",
        "joined_ad_domain": False,
        "mac_lack_full_disk_access": None,
        "mac_lack_screenshot_access": None,
        "os_install_date": 0,
        "mac_mdm_profile_installed": None
    }
    ios_report_info = {
        "memory_total": 3662,
        "memory_available": 1106,
        "disk_total": 121947,
        "disk_available": 94631,
        "cpu_arch": 0,
        "cpu_model": "A14",
        "gpu_model": "",
        "nic_type": "",
        "mac_addrs": [
            ""
        ],
        "login_user": "mobile",
        "is_vm": False,
        "serial_number": "",
        "licensed_windows": False,
        "nic_detail_list": [
            {
                "nic_type": "ap1",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "lo0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "127.0.0.1",
                "ipv6": [
                    "::1",
                    "fe80::1"
                ]
            },
            {
                "nic_type": "pdp_ip4",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "pdp_ip5",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "utun0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": [
                    "fe80::9076:103d:db64:a15c"
                ]
            },
            {
                "nic_type": "utun1",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": [
                    "fe80::9e0f:6b:6fbe:38e7"
                ]
            },
            {
                "nic_type": "utun3",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": [
                    "fe80::ce81:b1c:bd2c:69e"
                ]
            },
            {
                "nic_type": "XHC0",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "en1",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "ipsec0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "ipsec1",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "en0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "10.79.153.44",
                "ipv6": [
                    "fe80::105e:534e:3139:149d",
                    "fdbd:ff1:ce00:2c7:c2f:8e66:37ac:898b",
                    "fdbd:ff1:ce00:2c7::fcc"
                ]
            },
            {
                "nic_type": "awdl0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::d82b:4cff:fe12:81dd"
                ]
            },
            {
                "nic_type": "llw0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": [
                    "fe80::d82b:4cff:fe12:81dd"
                ]
            },
            {
                "nic_type": "pdp_ip1",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "pdp_ip3",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "pdp_ip6",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "utun2",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": True,
                "ipv4": "",
                "ipv6": [
                    "fe80::567:357f:9147:4e14"
                ]
            },
            {
                "nic_type": "anpi0",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "pdp_ip0",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "pdp_ip2",
                "mac_addr": "",
                "active": False,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            },
            {
                "nic_type": "en2",
                "mac_addr": "",
                "active": True,
                "description": "",
                "is_virtual": False,
                "ipv4": "",
                "ipv6": None
            }
        ],
        "hdd_serial_numbers": None,
        "ssd_serial_numbers": None,
        "cpu_serial_number": "",
        "mem_serial_numbers": None,
        "windows_ad_domain_name": "",
        "windows_ad_domain_account": "",
        "joined_ad_domain": False,
        "mac_lack_full_disk_access": None,
        "mac_lack_screenshot_access": None,
        "os_install_date": 0,
        "mac_mdm_profile_installed": None
    }
    report_info_map = {
        "Mac": mac_report_info,
        "Windows": windows_report_info,
        "Linux": linux_report_info,
        "Android": android_report_info,
        "iOS": ios_report_info
    }
    report_info = report_info_map.get(os, mac_report_info)
    report_info_data = {
        "items": [],
        "new_login": True
    }
    for key, value in report_info.items():
        if key == "nic_detail_list":
            pass
        report_info_data["items"].append({"key": key, "value": value})
    nic_detail_list = report_info.get("nic_detail_list", [])
    nic_detail_data = {}
    for item in nic_detail_list:
        nic_detail_data[item.get("nic_type")] = {
            "active": item.get("active"),
            "mac_addr": item.get("mac_addr")
        }
    report_info_data["items"].append({"key": "nic_detail_list", "value": nic_detail_data})
    return report_info_data


def get_user_device_info(os):
    mac_device_info = {
        "app_version": "2.0.0",
        "brand": "Apple",
        "build_number": "1000",
        "language": "zh",
        "model": "MacBookPro16,2",
        "os": "Mac",
        "os_version": "14.0",
        "os_ver": "14.0",
        "soc": "Intel%28R%29+Core%28TM%29+i7-1068NG7+CPU+%40+2.30GHz",
    }
    windows_device_info = {
        "app_version": "2.0.0",
        "brand": "HUAWEI",
        "build_number": "1000",
        "language": "zh",
        "model": "KLVC-WXX9",
        "os": "Windows",
        "os_version": "Windows10_v10.0",
        "os_ver": "Windows10_v10.0",
        "soc": "Intel%28R%29+Core%28TM%29+i7-1068NG7+CPU+%40+2.30GHz",
    }
    linux_device_info = {
        "app_version": "2.0.0",
        "brand": "LENOVO",
        "build_number": "1000",
        "language": "zh",
        "model": "20UAA0SVCD",
        "os": "Linux",
        "os_version": "Ubuntu 20.04.3 LTS",
        "os_ver": "Ubuntu 20.04.3 LTS",
        "soc": "Intel%28R%29+Core%28TM%29+i7-1068NG7+CPU+%40+2.30GHz",
    }
    android_device_info = {
        "app_version": "2.0.0",
        "brand": "HUAWEI",
        "build_number": "1000",
        "language": "zh",
        "model": "NOH-AL10",
        "os": "Android",
        "os_version": "31",
        "os_ver": "31",
        "soc": "Intel%28R%29+Core%28TM%29+i7-1068NG7+CPU+%40+2.30GHz",
    }
    ios_device_info = {
        "app_version": "2.0.0",
        "brand": "Apple",
        "build_number": "1000",
        "language": "zh",
        "model": "iPhone 12",
        "os": "iOS",
        "os_version": "17.2",
        "os_ver": "17.2",
        "soc": "Intel%28R%29+Core%28TM%29+i7-1068NG7+CPU+%40+2.30GHz",
    }
    info_map = {
        "Mac": mac_device_info,
        "Windows": windows_device_info,
        "Linux": linux_device_info,
        "Android": android_device_info,
        "iOS": ios_device_info
    }
    return info_map.get(os, mac_device_info)


def get_login_headers(user_name, password, device_id, device_name, login_user_device_info):
    lookup_url = "https://{}:{}/api/lookup".format(host, fe_port)
    login_url = "https://{}:{}/api/demo".format(host, fe_port)
    setting_url = "https://{}:{}/api/setting".format(host, fe_port)
    data = {
        "user_name": user_name,
        "password": sha256(password),
        "platform": ""
    }
    session = requests.Session()
    session.cookies.update({"device_id": device_id, "device_name": device_name})
    lookup_response = session.post(url=lookup_url, params=login_user_device_info, json=data, verify=False)
    session.cookies.update(lookup_response.cookies)
    login_response = session.post(url=login_url, params=login_user_device_info, json=data, verify=False)
    session.cookies.update(login_response.cookies)
    session.headers["csrf-token"] = re.findall("csrf-token=(.*?) ", str(session.cookies))[0]
    cookie = "; ".join(["{}={}".format(item[0], item[1]) for item in session.cookies.items()])
    csrf_token = session.headers["csrf-token"]
    session.get(url=setting_url, params=login_user_device_info, verify=False)
    headers = {
        "cookie": cookie,
        "csrf-token": csrf_token
    }
    return headers


def before_run(cache, test_info, test_case):
    return test_info, test_case


def after_run(cache, test_info, test_case, data, responses):
    login_info = test_case.get("login_info")
    login_user_name, login_os_str = login_info.split(":")
    login_os_list = login_os_str.split("_")
    login_user_mobile = test_case.get("parameter").get("user").get("mobile")
    login_user_id = data.get("data").get("user_id")
    login_user_start_password = get_user_start_password(login_user_id)
    cache.set("{}_uid".format(login_user_name), login_user_id)
    for login_os in login_os_list:
        login_user_device_name = "apitest_device_{}".format(generate_str())
        login_user_device_id = generate_did()
        cache.set("{}_{}_device_name".format(login_user_name, login_os), login_user_device_name)
        cache.set("{}_{}_device_did".format(login_user_name, login_os), login_user_device_id)
        login_user_device_info = get_user_device_info(login_os)
        user_login_headers = get_login_headers(login_user_mobile, login_user_start_password, login_user_device_id,
                                               login_user_device_name, login_user_device_info)
        report_url = "https://{}:{}/api/device/report".format(host, fe_port)
        device_report_info = get_device_report_info(login_os)
        response = requests.post(url=report_url, params=login_user_device_info, json=device_report_info,
                                 headers=user_login_headers)
        cache.set("{}_{}_login_headers".format(login_user_name, login_os), user_login_headers)
        print(response.json())
