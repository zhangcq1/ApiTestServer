# -*- coding:utf-8 -*-
import random
import time


def generate_phone():
    # 基于三大运营商号段+随机数生成伪手机号
    ctcc = [133, 153, 173, 177, 180, 181, 189, 191, 193, 199]
    cucc = [130, 131, 132, 155, 156, 166, 175, 176, 185, 186, 166]
    cmcc = [134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198]
    begin = 10 ** 7
    end = 10 ** 8 - 1
    prefix = random.choice(ctcc + cucc + cmcc)
    return str(prefix) + str(random.randint(begin, end))


def generate_email():
    # 基于手机号生成邮箱
    email_type = [
        "@gmail.com", "@yahoo.com", "@msn.com",
        "@hotmail.com", "@aol.com", "@ask.com",
        "@live.com", "@qq.com", "@0355.net", "@yeah",
        "@163.com", "@163.net", "@263.net", "@3721.net"
    ]
    phone = generate_phone()
    email = phone + random.choice(email_type)
    return email


def generate_mac():
    # 基于手机号生成mac 地址
    mac = [random.randint(0x00, 0x7f) for i in range(6)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def generate_ip():
    # 基于手机号生成ip地址
    ip = [str(random.randint(0, 255)) for i in range(4)]
    return '.'.join(ip)


def generate_did():
    # 基于手机号生成设备did
    device_id = ''.join([random.choices("abcedfghijklmnopqrstuvwxyz0123456789")[0] for i in range(32)])
    return device_id


def generate_str():
    # 基于手机号生成随机字符串
    random_str = ''.join([random.choices("abcedfghijklmnopqrstuvwxyz0123456789")[0] for i in range(4)])
    return random_str


def generate_now_timestamp():
    # 生成当前时间戳
    now_timestamp = str(int(time.time()))
    return now_timestamp


def generate_week_timestamp():
    # 生成一周后时间戳
    week_timestamp = str(int(time.time()) + 60 * 60 * 24 * 7)
    return week_timestamp


if __name__ == '__main__':
    # 生成常用数据
    print(generate_phone())
    print(generate_email())
    print(generate_mac())
    print(generate_ip())
    print(generate_did())
    print(generate_str())
    print(generate_now_timestamp())
    print(generate_week_timestamp())
