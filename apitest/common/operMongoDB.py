# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:55 上午
# @Author  : Hui
# @File    : operMongoDB.py

"""
    操作mongoDB工具类
        * 提供 select,insert_batch,insert_one,update_batch,delete_batch
        * 示例调用
            operMongoDB = OperMongoDB(host='172.16.64.101',port=27017,db_name='relation-center',username='admin',password='admin',auth_source='admin')

            insertdata = {'userId': 131000000000000000, 'friendId': 131000000000000001, 'relationId': 131000000000000004, 'companyId': 139000000000000004,
                'relationType': 1, 'relationStatus': 0, 'sourceType': 0, 'sourceDecs': 'APITest'}
            result = operMongoDB.insert_one("relationship",param=insertdata)
            logger.debug(result)

            query_data = {'userId':131000000000000000,'sourceDecs': 'APITest'}
            update_data = {"sourceDecs": "APITester"}
            result = operMongoDB.update_batch("relationship",query=query_data,param=update_data)
            logger.debug(result)

            # qurey = {"userId":{"$gt":522177881971889900}}
            query_param = {"userId":131000000000000000}
            result = operMongoDB.select(collection="relationship",param=query_param)
            logger.debug(result)

            delete_data = {"sourceDecs": "APITester"}
            result = operMongoDB.detele_batch("relationship",param=delete_data)
            logger.debug(result)
            operMongoDB.close()
"""
import pymongo
from common.logUtils import logger


class OperMongoDB:

    def __init__(self, host, port, db_name, username=None, password=None, auth_source="admin", auth_mechanism='SCRAM-SHA-1'):
        '''
        连接mongodb,authSource为认证数据库名，若无认证则可不填
        :param host: 主机名
        :param port: 端口号
        :param db_name:
        :param username:
        :param password:
        :param authSource: 认证数据库名 admin
        :param authmechanism: mechanism为认证机制，mongdb 3.0及以后的版本使用SCRAM-SHA-1，3.0以下则使用MONGODB-CR
        '''
        try:
            # auth_mechanism 选择了这个可能会报错 authentication fail，真是无语
            if username and password:
                self.client = pymongo.MongoClient(host, port, username=username, password=password,
                                                  authSource=auth_source, authMechanism=auth_mechanism)
            else:
                self.client = pymongo.MongoClient(host, port)
            self.db = self.client.get_database(db_name)
            # LogUtils.debug("数据库连接成功！")
        except Exception as e:
            logger.debug("数据库连接失败！")
            print(e)

    def select(self, collection, sort=0, sortname=None, param=None):
        """
        查询
        :param collection:表名
        :param param: 语句
        :param sort: 排序，1为升序 -1为降序
        :param sortname:排序key
        :return: list
        """
        if (isinstance(param, dict) or param is None) and isinstance(sort, int):
            cursor = self.db.get_collection(collection).find(param)
            if (int(sort) == 1 or int(sort) == -1) and sortname is not None:
                cursor.sort(sortname, sort)
            return list(cursor) if cursor.count() != 0 else []
        else:
            raise Exception("param 类型错误，请传入dict类型")

    def insert_one(self, collection, param):
        """
        增加数据
        :param collection: 表名
        :param param: list
        :return:
        """
        if isinstance(param, dict):
            data = self.db.get_collection(collection).insert_one(param)
            return data.inserted_id
        else:
            raise Exception("param类型错误，请传list类型")

    def insert_batch(self, collection, param):
        """
        增加数据
        :param collection: 表名
        :param param: list
        :return:
        """
        if isinstance(param, list):
            data = self.db.get_collection(collection).insert_many(param)
            return data.inserted_ids
        else:
            raise Exception("param类型错误，请传list类型")

    def update_batch(self, collection, query, param):
        """
        批量修改数据
        :param collection:表名
        :param param:
        :return:
        """
        if type(param) and isinstance(param, dict):
            new_values = {"$set": param}
            logger.debug(new_values)
            result = self.db.get_collection(collection).update_many(query, new_values)
            return result.modified_count
        else:
            raise Exception("参数类型异常")

    def detele_batch(self, collection, param):
        """
        批量删除 param is not None
        :param collection: 表名
        :param param:删除匹配的数据
        :return:
        """
        if param is not None and isinstance(param, dict):
            result = self.db.get_collection(collection).delete_many(param)
            return result.deleted_count
        else:
            raise Exception("参数类型异常")

    def close(self):
        """
        关闭资源
        :return:
        """
        if self.client is not None:
            self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    db_msg = {
        "host": '192.168.3.120',
        "port": 27017,
        "username": 'admin',
        "password": 'admin',
        # 写成下面这样是得罪了谁，一直报错  'Authentication failed.'？？？？
        # "username": "﻿admin",
        # "password": "﻿admin",
        "db_name": "test"
    }
    collection_name = 'ai_card'
    query = {"card_name": "matthewmarquez"}

    with OperMongoDB(**db_msg) as op:
        res = op.select(collection=collection_name, param=query)
        print(res)
