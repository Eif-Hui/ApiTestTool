# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 4:13 下午
# @Author  : Hui
# @File    : assertUtils.py
from common.logUtils import logger
import re

assert_methods = {
            "expect": 'assertEqual',
            "equal": 'assertEqual',
            "notEqual": 'assertNotEqual',
            "in": 'assertIn',
            "notIn": 'assertNotIn'
        }


def assert_equals(actual, expected):
    """
    断言是否等于
    :param actual: 实际值
    :param expected: 预期值
    :return:
    """
    try:
        assert actual == expected
        logger.info("断言成功,实际值：{} 等于 预期值：{}".format(actual, expected))
    except AssertionError as e:
        logger.error("断言失败,实际值：{} 不等于 预期值：{}".format(actual, expected))
        raise AssertionError


def assert_true(actual):
    """
    断言是否为真
    :param actual: 实际值
    :return:
    """
    try:
        assert actual == True
        logger.info("断言成功,实际值：{} 为真".format(actual))
    except AssertionError as e:
        logger.error("断言失败,实际值：{} 不为真".format(actual))
        raise AssertionError


def assert_in(content, target):
    """
    断言是否包含
    :param content: 包含文本
    :param target: 目标文本
    :return:
    """
    try:
        assert content in target
        logger.info("断言成功,目标文本：{} 包含 文本：{}".format(target, content))
    except AssertionError as e:
        logger.error("断言失败,目标文本：{} 不包含 文本：{}".format(target, content))
        raise AssertionError


def assert_regexp(check_data, resp_data):
    """
    :param check_data: 表达是，对象
    :param resp_data:
    :return:
    """
    if re.findall(check_data, resp_data):
        return True
    else:
        return False


