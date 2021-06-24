# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 8:53 AM
# @Author  : Hui
# @File    : helper.py
import importlib
import os
import re
import string
import sys
import unittest

import faker

from config.constans import test_dir
from common.logUtils import LogUtils

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))
# 函数助手用
default_elements = string.ascii_letters + string.digits
f = faker.Faker()


def find_ergodic_test_dir(test_dir):
    """
    遍历发现测试文件夹
    :param test_dir:
    :return:
    """
    case_list = list()
    dir_list = os.listdir(test_dir)
    for _dir in dir_list:
        if 'test_project_01' in _dir:
            case_list.append(test_dir + '/' + _dir)
        elif '.' not in _dir:
            case_list_dir = find_ergodic_test_dir(test_dir + '/' + _dir)
            if len(case_list_dir) > 0:
                case_list.extend(case_list_dir)
    return case_list


def find_cases(test_dir, pattern):
    """发现测试用例集"""
    suite = unittest.TestSuite()
    case_dir = find_ergodic_test_dir(test_dir)
    for _dir in case_dir:
        s = os.path.join(_dir)
        sys.path.append(s)
        loader = unittest.TestLoader()
        discover = loader.discover(start_dir=_dir, pattern=pattern)
        suite.addTests(discover)
    return suite


def exists_pub_case(run_proj, public_case_name='public_case.py'):
    """判断公共用例是否存在"""
    if public_case_name in os.listdir(test_dir + run_proj):
        return True
    return False


def find_public_class(run_proj):
    """探索用例文件"""
    module_name = 'test_project_01.{}.public_case'.format(run_proj)  # 模块名的字符串
    _class = importlib.import_module(module_name)  # 导入的就是需要导入的那个metaclass
    return _class.PublicCase  # 调用下面的方法


def run_pub_case(run_class):
    """运行公共用例"""
    if run_class:
        try:
            suite = unittest.TestSuite()
            suite.addTests(unittest.makeSuite(run_class))
            runner = unittest.TextTestRunner()
            LogUtils.debug(f'检测到{suite.countTestCases()}条公共用例，开始执行公共用例：')
            res = runner.run(suite)

            if res.errors or res.failures:
                LogUtils.error("公共用例运行失败，请检查公共用例配置！")
                sys.exit(-1)

            LogUtils.error("公共用例运行成功！")
        except Exception as e:
            LogUtils.error("公共用例运行失败，请检查公共用例配置！")
            LogUtils.error(e)
            sys.exit(-1)


def random_randint(min_=1, max_=100):
    return f.random.randint(min_, max_)


def random_letters(length=10):
    return ''.join(f.random_letters(length=length))


def random_sample(elements=default_elements, length=10):
    return ''.join(f.random_choices(elements=str(elements), length=length))


random_dict = {"randint": random_randint, 'letters': random_letters, 'sample': random_sample}


def random_help(name: str, pattern='\$\{Random_(.*)\((.*)\)\}'):
    """
    随机函数助手，输出以下常用随机数，返回结果值。支持函数:
        1、random_randint(min=1, max=100)    返回范围内整数，默认范围1～100
        2、random_letters(length=10)         返回大小写字母组成的指定长度字符串，默认长度10
        3、random_sample(elements=string.letters+string.digits, length=10)   # 返回指定字符串，默认由大小写+数字组成，长度为10
    :param name:  函数名，需要在 randint、letters、sample 之间
    :param pattern:  匹配模式
    :return:  随机函数调用结果 or None
    """
    try:
        m = re.match(pattern, name)
        key, value = m.groups()
        if random_dict.get(key):
            func = random_dict[key]
            _param = [eval(x) if x.strip().isdigit() else x for x in value.split(',')]
            return str(func.__call__(*_param))
        LogUtils.error(f'不支持的函数 {name}, 请检查函数名是否正确！')
    except Exception as e:
        LogUtils.error(f'{name} 函数解析异常: {e}')


if __name__ == '__main__':
    print(random_help('${Random_randint(1, 10)}'))
    print(random_help('${Random_letters(5)}'))
    print(random_help('${Random_sample(1234567890abc, 30)}'))
    print(random_help('${Random_sample(1234567890abc, 30)}'))
