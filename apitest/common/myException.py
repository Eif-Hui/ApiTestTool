# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 8:53 AM
# @Author  : Hui
# @File    : myException.py


class AssertKeyNotFoundError(Exception):
    """ AssertKey not found. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class AssertMethodNotFoundError(Exception):
    """ AssertMethod not found. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class DataCheckArgsError(Exception):
    """ DataCheck args is err. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class DataCheckFail(Exception):
    """ DataCheck fail. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class ValidatorKeyNotFoundError(Exception):
    """ ValidatorKey not found. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class HTTPError500(Exception):
    """ http响应500+错误 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class HTTPError400(Exception):
    """ http响应400+错误 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class HTTPNullResponseException(Exception):
    """ http无响应错误 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class RelationDataGetException(Exception):
    """ 关联提取失败 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class ResponseAssertCheckException(Exception):
    """ 响应断言异常 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class DataCheckException(Exception):
    """ 数据校验异常 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class HTTPResponseException(Exception):
    """ http响应异常 """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass
