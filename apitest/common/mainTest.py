# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 12:18 下午
# @Author  : Hui
# @File    : mainTest.py


import requests
from common.logUtils import logger
from common.assertUtils import *
from string import Template
from json import dumps
import time
import jsonpath
import re
import json


class RequestUtil(requests.Session):
    def __init__(self):
        super().__init__()
        self.variable_pool = {}  # 定义变量池
        self.retry_num = 0  # 定义初始次数

    def send_request(self, method, url, case_desc=None, verification=None, jsonpath_exp=None, regular_exp=None,
                     **kwargs):

        before_time = time.time()
        for k, v in kwargs.items():
            kwargs[k] = self.replace_template_str(v)
            try:
                kwargs[k] = json.loads(v)
            except:
                pass

        logger.info('*** requests front ***'.center(80, "-"))
        logger.info(f"case desc：{case_desc}")
        logger.info(f"JsonPath 表达式： {jsonpath_exp}")
        logger.info(f"Re 正则表达式： {regular_exp}")
        logger.info(f"Api 断言表达式： {verification}")
        logger.info(f'requests.method : {method}')
        logger.info(f'requests.url : {url}')
        for k, v in kwargs.items():
            logger.info(f'requests.data : {k}：{v}')

        response = super().request(method, url, **kwargs)
        after_time = time.time()

        if response.status_code == 200:
            logger.info(f"time consuming: {after_time - before_time} s\n")
        else:
            if self.retry_num > 2:
                self.retry_num = 0
                logger.info("接口请求失败，重试完毕！")
                return response
            logger.info(f"接口请求失败，响应code为 {response.status_code}, 进行第 {self.retry_num + 1} 次重试")
            self.retry_num += 1
            self.send_request(method, url, **kwargs)

        logger.info('*** response behind ***'.center(80, "-"))
        logger.info(f'response.status_code : {response.status_code}')
        logger.info(f'response.headers : {response.headers}')
        logger.info(f'response.text : {response.text}')

        if verification:
            if verification.endswith(";"):
                verification = verification.split(";")[0]
            for ver in verification.split(";"):
                expr = ver.split("=")[0]
                # 判断Jsonpath还是正则断言
                if expr.startswith("$."):
                    actual = jsonpath.jsonpath(response.json(), expr)
                    if not actual:
                        logger.error("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性1")
                    actual = actual[0]
                else:
                    actual = re.findall(expr, response.text)[0]
                expect = ver.split("=")[1]
                assert_equals(str(actual), expect)

        if jsonpath_exp:
            for item in jsonpath_exp.split(";"):
                kvs = item.split("=")
                key = kvs[0]  # 获取关键字
                value = kvs[1]  # 获取jsonpath
                self.save_variable(response.text, key, jsonpath_expression=value)  # 进行JSONPATH提取并保存
        if regular_exp:
            for item in regular_exp.split(";"):
                kvs = item.split("=")
                key = kvs[0]  # 获取关键字
                value = kvs[1]  # 获取正则表达式
                self.save_variable(response.text, key, regular_expression=value)  # 进行正则提取并保存

        logger.info("*** requests end ***".center(80, "-"))
        return response

    def replace_template_str(self, target):
        target = str(target)
        # 正则匹配所有{{key}}，并做处理
        EXPR = r'\$\{(.*?)\}'
        keys = re.findall(EXPR, str(target))
        if keys:
            logger.info(f"变量池中匹配到需替换的参数: {keys}")
        for key in keys:
            value = self.variable_pool.get(key)
            if not value:
                logger.warning("变量池中未匹配到关联参数！不进行替换操作")
                continue
            target = target.replace('${' + key + '}', str(value))
            logger.info("替换了{" + key + "} 为：" + str(value))

        # 遍历所有函数助手并执行，结束后替换
        FUNC_EXPR = r'__.*?\(.*?\)'
        funcs = re.findall(FUNC_EXPR, str(target))
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name, fuc_name.lower())
            value = eval(fuc)
            target = target.replace(func, str(value))
        try:
            target = eval(target)
        except:
            target = target
        return target

    def save_variable(self, target, key, jsonpath_expression=None, regular_expression=None):
        """
        存储变量到变量池
        :param target: 目标字符串
        :param key: 关键字
        :param jsonpath_expression: JSONPATH表达式
        :param regular_expression: 正则表达式
        :return:
        """
        match_values = jsonpath.jsonpath(json.loads(target),
                                         jsonpath_expression) if jsonpath_expression else re.findall(
            regular_expression, target)
        if match_values:
            value = match_values[0]
            self.variable_pool[key] = value
            logger.info(f"保存了变量 {key} --> {value} 到 变量池, 当前变量池参数 {str(self.variable_pool)}")
            return value
        else:
            logger.warning("未匹配到任何参数，不进行保存！")

            return


BaseRequests = RequestUtil()

# BaseRequests.replace_template_str("{'Accept': 'application/json, text/plain, */*', 'Authorization': 'Bearer ${token}'}")
# if __name__ == '__main__':
#     request_util = RequestUtil()
#     body = {
#         "password": "123456",
#         "userName": "admin"
#     }
#
#     request_util.send_request("post", "http://39.105.34.24:8080/apis/login", desc="登入账户", json=body)
#     body = {
#         "isTiming": 0,
#         "taskName": "test1",
#         "taskDesc": "测试1",
#         "isParallel": 0,
#         "testSets": "[]",
#         "times": 3,
#         "isDing": 0,
#         "dingId": ""
#     }
#     # headers = {
#     #     "Cookie": "JSESSIONID=" + jsession_id
#     # }
#     request_util.send_request("post", "http://39.105.34.24:8080/apis/task/", desc="新增普通任务", json=body)  # 新增普通任务
#
#     params = {
#         "taskName": "",
#         "isParallel": ""
#     }
#     response = request_util.send_request("get", "http://39.105.34.24:8080/apis/task/1", desc="查询普通任务,并保存taskId",
#                                          jsonpath_exp="taskId=$.data.list[0].taskId", params=params)
#     response = request_util.send_request("delete", "http://39.105.34.24:8080/apis/task/{{taskId}}", desc="根据task_id "
#                                                                                                          "删除普通任务")
