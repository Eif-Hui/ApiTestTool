# -*- encoding: utf-8 -*-
"""
@File    : read_data.py
@Time    : 2021/2/26 9:27
@Author  : xiewenhui
@Email   : xiewenhui@deepexi.com
@Software: PyCharm
"""
from common.logUtils import logger
import yaml, json
import pprint

pr = pprint.PrettyPrinter(indent=0)


def load_json(file_path):
    logger.info("加载 {} 文件......".format(file_path))
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    logger.info("读到数据 ==>>  {} ".format(data))
    return data


def load_yaml(file_path):
    logger.info("加载 {} 文件......".format(file_path))
    with open(file_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data, indent=4))
    logger.info("读到数据 ==>>  {} ".format(data))
    return data


from config.constans import *

# yaml_dir = test_dir + 'test_project_01/data/collection.yaml'
# load_yaml(yaml_dir)
