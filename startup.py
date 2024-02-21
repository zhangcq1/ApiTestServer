# -*- coding:utf-8 -*-
import logging
import sys
import concurrent.futures
import warnings
from comm.script import writeLogs, writeCaseYml, writeConfig
from config import *
warnings.filterwarnings('ignore')


def thread_run(func, thread_num, args=None):
    # 创建一个线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交n个任务给线程池
        args = [args] * thread_num  # 指定函数参数
        futures = [executor.submit(func, arg) for arg in args]
        # 获取任务的结果
        for future in concurrent.futures.as_completed(futures):
            future.result()


def task_apitest(conf):
    # TEST_API_DIR : 接口测试脚本
    # TEST_FLOW_DIR : 场景测试脚本
    run_type = conf.get("run_type")
    run_module = conf.get("run_module", "")
    run_module_list = run_module.split("_")
    test_file = []
    if run_type == "test_api":
        script_dir = TEST_API_DIR
    else:
        script_dir = TEST_FLOW_DIR
    if run_module == "all":
        test_file.append(script_dir)
    else:
        for run_module in run_module_list:
            run_module_script = "{}/test_{}.py".format(script_dir, run_module)
            test_file.append(run_module_script)
    args_list = [
        '-vs',
        '-n', str(RC['process']),
        '-m', conf.get("version", "saas"),  # 指定类型
        '--reruns', str(RC['reruns']),
        '--maxfail', str(RC['maxfail']),
        '--alluredir', REPORT_DIR + '/xml',
        '--junit-xml', REPORT_DIR + '/junit.xml',
        '--clean-alluredir',
        '--disable-warnings'
    ]
    args_list.extend(test_file)
    pytest.main(args_list)
    # 生成allure报告
    cmd = 'allure generate --clean %s -o %s ' % (REPORT_DIR + '/xml', REPORT_DIR + '/html')
    os.system(cmd)
    clear(1)
    return 1


def task_performance(conf):
    # TEST_PERFORMANCE_DIR : 压力测试脚本
    pass


def task_other(conf):
    # TEST_OTHER_DIR : 造数/其他测试脚本
    run_module = conf.get("run_module")
    func_map = {
        "create": create_all,
        "clear": clear
    }

    thread_num = int(conf.get("thread_num", "1"))
    task_num = int(conf.get("task_num", "1"))
    if run_module and func_map.get(run_module):
        if run_module != "create":
            thread_num, task_num = 1, 1
        thread_run(func_map.get(run_module), thread_num, args=task_num)
    return 1


def task_none(conf):
    print("run_type参数有误，请重新检查运行参数")


def run(conf):
    # 开启日志记录(默认logs目录)
    print("运行配置：{}".format(conf))
    writeLogs.MyLogs(ROOT_DIR + 'logs')
    task_map = {
        "test_api": task_apitest,
        "test_flow": task_apitest,
        "test_performance": task_performance,
        "test_other": task_other,
        "none": task_none
    }
    # 判断运行模式
    # RC['auto_switch']=1
    if RC['auto_switch'] == 1:
        logging.info("根据接口抓包数据，自动生成测试用例和测试脚本，但不运行测试！")
        writeCaseYml.write_case_yaml(DATA_DIR)
        sys.exit(0)
    else:
        logging.info("不开启自动生成测试用例功能，将直接运行测试！")
    # 重写apiConfig文件，端口、域名、登录态等
    writeConfig.write_config(conf)
    run_type = conf.get("run_type", "none")
    task_map.get(run_type)(conf)


if __name__ == '__main__':
    # 通用参数: 其中run_type，domain必传
    # run_type : test_api 接口测试，test_flow 场景测试，test_performance 性能测试(开发中)，test_other 造数据/清数据(开发中)
    # domain : 环境域名或ip(例：corplink-boe.ifeilian.cn/10.2.6.185)
    # fe_port: 门户端口(默认10443)
    # admin_port: 管理后台端口(默认8443)
    # admin_user: 管理员账号(默认: admin@feilian.local)
    # admin_pwd: 管理员密码(默认: admin=corplink2020!)
    # 接口自动化参数
    # run_module(test_api,test_flow使用) : all(默认)，
    # identity(身份管理)，device(终端管理)，software(软件管理)，application(应用管理)，vpn(vpn管理)，wifi(wifi管理)，baseline(终端基线)，dlp(数据防泄漏)
    # antivirus(防病毒)，dynamic(动态控制)，it(IT应用)，configuration(通用配置)，integration(集成管理)，settings(系统设置)，license(权益中心)，versions(版本发布)，third(数据源同步)
    # domain : 环境域名或ip(例：corplink-boe.ifeilian.cn/10.2.6.185)
    # version : saas(SaaS版本,默认)，private(私有化版本)
    # 性能测试参数

    # 造数据/清数据参数
    # run_module : create(造数据)、clear(清数据)
    # thread_num : 执行线程数(默认1)
    # task_num : 每个线程执行任务数(默认1)

    # 本地生成测试报告，仅接口自动化
    # allure open -h 127.0.0.1 -p 8003 ./project/report/
    args = sys.argv[1:]
    # 造数示例
    # args = ["run_type=test_other", "run_module=baseline", "domain=apitest.feilian.cn", "version=saas",
    #         "thread_num=1", "task_num=1", "fe_port=443", "admin_port=443", "admin_user=", "admin_pwd="]
    # 自动化示例
    # args = ["run_type=test_api", "run_module=application", "domain=corplink-boe.ifeilian.cn", "version=saas",
    #         "fe_port=", "admin_port=", "admin_user=", "admin_pwd="]
    run_conf = {item.split("=")[0]: "=".join(item.split("=")[1:]) for item in args}
    run(run_conf)
