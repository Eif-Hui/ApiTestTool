# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 8:53 AM
# @Author  : Hui
# @File    : debug_var_utils.py
import re

from jsonpath import jsonpath
import copy

from common.debugVar import DebugVar
from common.helper import random_help
from common.myException import RelationDataGetException


class DebugVarUtils:
    """
    获取变量值的工具类
    """

    @classmethod
    def get_debug_var_value_dict(cls, param):
        """从dict中提取并替换参数变量"""
        if isinstance(param, dict):
            for key, value in param.items():
                if isinstance(value, dict):
                    cls.get_debug_var_value_dict(value)
                elif isinstance(value, list):
                    _tmp = cls.get_debug_var_value_list(value)
                    param[key] = _tmp
                else:
                    _tmp = cls.get_debug_value(value)
                    param[key] = _tmp
        elif isinstance(param, list):
            param = cls.get_debug_var_value_list(param)
        else:        # ${param} in url: /a/${b}/${c}
            param = cls.get_debug_value(param)
        return param

    @classmethod
    def get_debug_var_value_list(cls, value, _resp=''):
        """从list中提取并替换参数变量"""
        if not _resp:
            _resp = []
        for x in value:
            if isinstance(x, dict):
                _tmp = cls.get_debug_var_value_dict(x)
            elif isinstance(x, list):
                _tmp = cls.get_debug_var_value_list(x)
            else:
                _tmp = cls.get_debug_value(x)
            _resp.append(_tmp)
        return _resp

    @classmethod
    def get_debug_value(cls, value):
        """
        取出指定变量名，支持随机取值
        """
        key_pattern = '\$\*|\${Random\_|\${'
        if not re.findall(key_pattern, str(value)):
            return value

        key_value = copy.deepcopy(value)
        if "$*" in str(value):  # 取值变量
            key_var = str(value).split("$*")[1]
            key_value = DebugVar.debug_vars.get(key_var)
        elif "${Random_" in str(value):  # random
            rand_pattern = "\$\{.*?\}"
            key_rand_col = re.findall(rand_pattern, value)
            if key_rand_col:
                for key_rand in key_rand_col:
                    _repl = random_help(key_rand)
                    key_value = key_value.replace(key_rand, _repl, 1)
        else:  # "${" in str(value)
            var_list = re.findall(r'\$\{(.*?)\}', key_value)
            for key in var_list:
                if key in DebugVar.debug_vars.keys():
                    key_value = key_value.replace("${%s}".strip(" ") % key, str(DebugVar.debug_vars.get(key)))
        return key_value

    @classmethod
    def extractor_var(cls, key, resp, _path=""):
        """
        提取变量（提取关联的数据给key），保存值到 DebugVar.debug_vars
        :param key: 需要赋予值的key名
        :param resp: 响应体
        :param _path: 需要获取的key值所在res中的path路径，如 a.b[index].c,或a.b[index].c[_index]
        :return:
        """
        try:
            if _path.startswith('re_search('):
                # re_search(pattern:str->expr, string:str->_path)
                res_ = re.search(r're_search\((.*?),(.*?)\)', _path)
                if res_:
                    expr, _path = [item.strip() for item in res_.groups()]
                    result = jsonpath(resp, '$..%s' % _path).pop().strip()
                    if '?P<target>' in expr:
                        result = re.search(expr, result).groupdict().get('target')
                    else:
                        result = re.search(expr, result).groups()[0]
                    # print(result, len(result))
                else:
                    print(f"关联错误！key={key}提取表达式({_path})失败！")
                    return
            else:
                result = jsonpath(resp, '$..%s' % _path).pop()

            DebugVar.debug_vars[key] = result
        except Exception as e:
            print(f"关联错误！key={key}提取关联路径({_path})失败！")
            print(e)
            raise RelationDataGetException


if __name__ == "__main__":
    res = {
        "token": 11111,
        "data": {
            "userId": "test_user_id",
            "companyId": "test_company_id",
            "c": [
                {
                    "c1": 1,
                    "c2": [1111, 2222]
                },
                {
                    "c3": 2,
                }
            ]
        }

    }

    # 关联值提取
    DebugVarUtils.extractor_var("i-token", res, "token")
    DebugVarUtils.extractor_var("userId", res, "data.userId")
    DebugVarUtils.extractor_var("companyId", res, "data.companyId")
    DebugVarUtils.extractor_var("c1", res, "data.c[0].c1")
    DebugVarUtils.extractor_var("c2", res, "data.c[0].c2[0]")
    # print(DebugVar.debug_vars)

    # 参数替换
    # _param = "/login/${userId}/${companyId}/${i-token}"
    # new_param = DebugVarUtils.get_debug_var_value_dict(_param)
    # print(new_param)
    #
    # _param = ['${userId}', 666, {'companyId': ['${companyId}']}]
    # l_param = DebugVarUtils.get_debug_var_value_dict(_param)
    # print(l_param)
    #
    # _param = {'userId': '${userId}', 'a': 666, 'data': {'companyId': '${companyId}'}}
    # d_param = DebugVarUtils.get_debug_var_value_dict(_param)
    # print(d_param)
    #
    # _param = {'userId': '${userId}', 'a': 666, 'data': {'companyId': {'cmd_1': '${companyId}'}}}
    # d_param = DebugVarUtils.get_debug_var_value_dict(_param)
    # print(d_param)

    _param = {'userId': '${userId}', 'a': 666, 'data': [{'companyId': ['${companyId}']}, {'companyId': '${companyId}'}]}
    d_param = DebugVarUtils.get_debug_var_value_dict(_param)
    print(d_param)

    _param = {'userId': '${userId}', "name": "burrows_${Random_letters(20)}_${Random_letters(20)}_test",
              "signature": "${Random_sample(123abc, 20)}", "age": "${Random_randint(10, 50)}",
              'data': [{'companyId': ['${companyId}']}, {'companyId': '${companyId}'}]}
    d_param = DebugVarUtils.get_debug_var_value_dict(_param)
    print(d_param)
