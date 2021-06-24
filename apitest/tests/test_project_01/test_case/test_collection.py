# -*- encoding: utf-8 -*-
"""
@File    : test_collection.py
@Time    : 2021/6/20 9:06
"""
import pytest
from common.mainTest import BaseRequests as R
from tests.test_project_01 import *
from config.setting import *


class TestCollection:

    @pytest.mark.datafile(yaml_dir + 'collection.yaml')
    def test_collection(self, parameters: dict):
        url = TEST_HOST + parameters.pop("url")
        method = parameters.pop("method")
        case_desc = parameters.pop("case_desc")
        variables = parameters.pop('jsonpath_exp')
        verification = parameters.pop('verification')
        R.send_request(method, url, case_desc=case_desc, verification=verification, jsonpath_exp=variables,  **parameters)


if __name__ == '__main__':
    pytest.main(['-s', '-k', 'test_collection.py'])
