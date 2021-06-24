# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:58 上午
# @Author  : Hui
# @File    : constans.py


import os

root_dir = os.path.abspath(os.path.curdir)  # 项目根文件夹
root_path = root_dir[:root_dir.find("apitest") + len("apitest")]  # 项目根路径

test_dir = root_path + '/tests/'  # 测试用例文件夹
test_report_dir = root_path + '/reports/'  # 测试报告文件夹


# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.abspath(os.path.dirname(__file__)[:-7])

# 定义测试用例的路径
TESTCASE_PATH = os.path.join(ROOT_PATH, 'tests')

# 定义测报告的路径
REPORT_PATH = os.path.join(BASE_PATH, 'reports')