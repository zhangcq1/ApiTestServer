# ApiTesting

### 框架介绍：
此框架是基于Python+Pytest+Requests+Allure+Yaml+Json实现全链路接口自动化测试。  

### 项目概述：
> **运行项目名** : 基于接口自动化实现接口测试、场景测试、压力测试、造数功能  
> **目录简介**:
> - comm
>  - db: 数据库操作&校验
>  - script: 文件操作脚本相关
>  - unit: 文件操作脚本相关
> - config: 配置相关
> - project: 测试项目名称
> - startup.py: 启动脚本


### 模版配置相关：
### 模版配置相关：
### 项目运行相关：


> 自动生成测试数据: config/runConfig.yml/auto_switch  
> - 0: 不开启自动生成测试用例功能，将直接运行测试
> - 1: 根据接口抓包数据，自动生成测试用例和测试脚本，但不运行测试
> 注意：目前解析仅支持(.chlsj)格式，请使用Charles工具抓包导出JSON Session File
> 测试模版说明：  
> 测试结果校验方式说明（共5种方式）：  
> - no_check：不做任何校验
> - check_code：仅校验接口返回码code
> - check_json：校验接口返回码code，并进行json格式比较返回结果（默认方式）
> - entirely_check：校验接口返回码code，并进行完整比较返回结果
> - regular_check：校验接口返回码code，并进行正则匹配返回结果

> 内置函数介绍： 
> - 生成一个伪手机号：$GenPhone()
> - 生成一个邮箱：$GenEmail()
> - 生成一个mac地址：$GenMac()
> - 生成一个IP地址：$GenIp()
> - 生成一个设备did：$GenDid()

> 校验/替换变量 关键词：type，类型指定如：integer/float/string/array/object/boolean
> 项目运行说明：  