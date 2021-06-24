# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:55 上午
# @Author  : Hui
# @File    : strUtils.py
import json
import time

from common.logUtils import LogUtils

from collections import Counter


class StrUtils:
    """
    字符串处理拓展工具类
    """

    @classmethod
    def is_json(cls, text):
        try:
            json.loads(str(text))
        except ValueError as e:
            LogUtils.debug(e)
            return False
        return True

    @classmethod
    def is_none(cls, text):
        return None if text == "null" or text == "" else text


class CreateEmailJson:
    """
    优化测试dict，便于构建email_html
    """

    def __init__(self, run_proj, child_proj):
        self.run_proj = run_proj
        self.child_proj = child_proj

    def optimize_test_result(self, res, pass_rate):
        """
        优化测试结果，便于输出邮件报告
        :param res:     测试统计结果 -> dict
        :return:        测试统计结果 -> dict
        """
        if isinstance(res, dict):
            test_apis, test_cases, test_fail_cases = self._count_test_result(res)
            res_new = {
                'testAll': res['testAll'],  # 测试总共请求数
                'testFail': res['testFail'],  # 测试失败请求数
                'testPass': res['testPass'],  # 测试通过请求数
                'testSkip': res['testSkip'],  # 测试忽略请求数
                'testError': res['testError'],  # 测试错误请求数
                "passRate": "%.2f%%" % pass_rate,  # 测试请求通过率
                'beginTime': res['beginTime'],
                'totalTime': res['totalTime'],
                'testCaseAll': len(test_cases),  # 测试总共用例数，1个用例为1个yaml文件，可包含多个测试请求，report中以 className 区分
                'testCaseFail': len(test_fail_cases),  # 测试失败用例数
                'testCaseFailDetail': f'{test_fail_cases}',
                "apiCounts": len(test_apis),  # 测试接口数
                "runProj": self.run_proj}

            test_failed = [test_info for test_info in res['testResult'] if test_info['status'] == '失败']
            from common.mainTest import RequestUtil
            test_pass_use_mock = [test_info['uri'] for test_info in res['testResult'] if
                                  MainTest.mock_flag in test_info['className']]

            # 错误等级分类
            rank_data = [x.get('rank') for x in test_failed]
            rank_classify = Counter(rank_data)
            res_new['errorLevel1'] = rank_classify.get("1") or 0
            res_new['errorLevel2'] = rank_classify.get("2") or 0
            res_new['errorLevel3'] = rank_classify.get("3") or 0
            res_new['testFailedResult'] = self._error_case_classify(test_failed)
            res_new['endTime'] = time.strftime("%Y-%m-%d %H:%M:%S")
            res_new['testPassUseMock'] = len(test_pass_use_mock)
            return res_new
        else:
            raise Exception("测试结果格式有误！")

    def _error_case_classify(self, test_failed):
        """
        根据接口名称分类统计
        :param test_failed:
        :return:
        """
        test_failed_dict = dict()
        test_failed_data = [x.get('className') for x in test_failed]
        test_failed_classify_count = Counter(test_failed_data)

        for test_failed_info in test_failed:
            class_name = test_failed_info['className']
            test_failed_info["errorLevel1"] = 0
            test_failed_info["errorLevel2"] = 0
            test_failed_info["errorLevel3"] = 0

            test_failed_info['testFail'] = test_failed_classify_count.get(class_name) or 0
            test_failed_info['project'] = self.child_proj
            rank = test_failed_info.get("rank")
            del test_failed_info['logs']
            del test_failed_info['methodName']
            if class_name not in test_failed_dict.keys():
                test_failed_dict[class_name] = test_failed_info
                test_failed_info["errorLevel%s" % rank] = 1
            else:
                test_failed_info["errorLevel%s" % rank] = test_failed_dict[class_name]["errorLevel%s" % rank] + 1
                test_failed_dict[class_name] = test_failed_info
            del test_failed_info['rank']
        return list(test_failed_dict.values())

    def _count_test_result(self, res):
        """
        计算测试接口数
        :param res:  测试统计结果 -> dict
        :return:     api地址集 -> set
        res demo
            {
                'testPass': 3,
                'testResult': [{
                    'className': 'login',
                    'methodName': '/arch-login-center/corp/list',
                    'description': '企管组织架构成员增删改-获取企管登陆信息',
                    'rank': 1,
                    'spendTime': '0.23 s',
                    'status': '成功',
                    'uri': '/arch-login-center/corp/list'
                    'logs': ['', '---------------------....
                }],
                'testName': '自动化测试报告',
                'testAll': 8,
                'testFail': 5,
                'beginTime': '2021-02-26 14:44:40',
                'totalTime': '7s',
                'testSkip': 0,
                'testError': 0
            }
        """
        # 测试接口总数，测试用例总数（yaml文件数），测试失败用例总数
        test_apis, test_cases, test_fail_cases = set(), set(), set()
        if isinstance(res, dict):
            for test_info in res['testResult']:
                test_apis.add(test_info['uri'])
                test_cases.add(test_info['className'])
                if test_info['status'] == '失败':
                    test_fail_cases.add(test_info['className'])
        return test_apis, test_cases, test_fail_cases


