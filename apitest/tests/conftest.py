# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 3:53 PM
# @Author  : Hui
# @File    : conftest.py

import json
import os
import yaml
from typing import List


def pytest_generate_tests(metafunc):
    ids = []
    markers = metafunc.definition.own_markers
    for marker in markers:
        if marker.name == 'datafile':
            test_data_path = os.path.join(metafunc.config.rootdir, marker.args[0])
            with open(test_data_path, encoding='utf-8') as f:
                ext = os.path.splitext(test_data_path)[-1]
                if ext in ['.yaml', '.yml']:
                    test_data = yaml.safe_load(f)
                elif ext == '.json':
                    test_data = json.load(f)
                else:
                    raise TypeError('datafile must be yaml or json，root must be tests')
    if "parameters" in metafunc.fixturenames:
        for data in test_data['tests']:
            ids.append(data['case_desc'])

        metafunc.parametrize("parameters", test_data['tests'], ids=ids, scope="function")


def pytest_collection_modifyitems(
        session: "Session", config: "Config", items: List["Item"]
) -> None:
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")
