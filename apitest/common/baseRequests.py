# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 8:54 AM
# @Author  : Hui
# @File    : test_base.py

import requests
from json import dumps
from common.logUtils import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseTest(requests.Session):

    def api_log(self, method, url, headers=None, params=None, json=None, cookies=None, file=None, code=None,
                res_text=None, res_header=None):
        logger.info('*** requests msg ***'.center(80, "-"))
        logger.info(
                    f'requests.method : {method}\n'
                    f'requests.url : {url}\n'
                    f'requests.headers : {dumps(headers,indent=0)}\n'
                    f'requests.data : {dumps(params or json, indent=4)}\n'
                    )
        logger.info('*** response msg ***'.center(80, "-"))
        logger.info(
                    f'response.status_code : {code}\n'
                    f'response.headers : {res_header}\n'
                    f'response.text : {res_text.decode("utf-8")}\n'
                    )

    def base_method(self, method, url, headers=None, params=None, data=None, json=None, cookies=None):
        # 判断接口请求类型
        if method.upper() == 'GET':
            '''
            get请求方法
            :param url: 地址
            :param headers: 请求头
            :param params: 请求参数
            :param cookies:
            :return:
            '''
            try:
                res = self.request('GET', url, headers=headers, params=params, cookies=cookies, verify=False)
                self.api_log('GET', url, headers=headers, params=params, cookies=cookies,
                             code=res.status_code, res_text=res.content, res_header=res.headers)
                return res
            except Exception as e:
                logger.error("接口请求异常,原因：{}".format(e))
                raise

        elif method.upper() == 'POST':
            """
                   post请求方法
                   :param url: 接口地址
                   :param headers: 请求头
                   :param json: 请求体
                   :param params: 请求参数
                   :param cookies:
                   :return:
                   """
            try:
                res = self.request('POST', url, headers=headers, params=params, data=data,
                                   json=json, cookies=cookies, verify=False)
                self.api_log('POST', url, headers=headers, params=params, json=json, cookies=cookies,
                             code=res.status_code, res_text=res.content, res_header=res.headers)
                return res

            except Exception as e:
                logger.error("接口请求异常,原因：{}".format(e))
                raise e
        elif method.upper() == 'DELETE':
            """
                   delete请求方法
                   :param url: 接口地址
                   :param headers: 请求头
                   :param json: 请求体
                   :param params: 请求参数
                   :param cookies:
                   :return:
                   """
            try:
                res = self.request('DELETE', url, headers=headers, params=params, data=data,
                                   json=json, cookies=cookies, verify=False)
                self.api_log('DELETE', url, headers=headers, params=params, json=json, cookies=cookies,
                             code=res.status_code, res_text=res.content, res_header=res.headers)
                return res

            except Exception as e:
                logger.error("接口请求异常,原因：{}".format(e))
                raise e
        elif method.upper() == 'PUT':
            """
                    put请求方法
                    :param url: 接口地址
                    :param headers: 请求头
                    :param json: 请求体
                    :param params: 请求参数
                    :param cookies:
                    :return:
                    """
            try:
                res = self.request('PUT', url, headers=headers, params=params, data=data,
                                   json=json, cookies=cookies, verify=False)
                self.api_log('PUT', url, headers=headers, params=params, json=json, cookies=cookies,
                             code=res.status_code, res_text=res.content, res_header=res.headers)
                return res

            except Exception as e:
                logger.error("接口请求异常,原因：{}".format(e))
                raise e


BaseRequests = BaseTest()
