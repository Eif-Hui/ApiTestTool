# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:55 上午
# @Author  : Hui
# @File    : operMysql.py
"""
    操作mysql数据库工具类
"""
import threading
import time
from datetime import datetime

import pymysql

from config.db_config import mysql_testplat
from common.logUtils import logger


class OperMysql:

    def __init__(self, host, port, user, passwd, dbname, charset='utf8'):
        try:
            self.conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=dbname, charset=charset)
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logger.debug("mysql数据库连接成功")
        except Exception as e:
            logger.error("mysql数据库连接失败!")
            print(e)

    def run(self, sql, rows=10):
        """
        查询语句，返回所有结果集
        :param sql:
        :param rows:行数
        :return: affected_rows,result
        """
        affected_rows = self.cursor.execute(query=sql)
        result = self.cursor.fetchmany(rows)
        self.conn.commit()
        return affected_rows, result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception:
            pass

    def insert_many(self, ins_sql,data_col: list):
        try:
            data_col = self.format_data(data_col)
            self.cursor.executemany(ins_sql, data_col)
            self.conn.commit()
        except Exception as e:
            print(f'Error！数据插入过程错误：{e}')
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()

    @staticmethod
    def format_data(src_data_col: list):
        data_col = []
        time_ns = time.time_ns()
        for item in src_data_col:
            _list = [time_ns, item.get('className'), item.get('methodName'), item.get('description'), item.get('rank'),
                     item.get('uri'), item.get('spendTime'), item.get('status'), item.get('logs')[0], datetime.now()]
            data_col.append(_list)
        return data_col


def res_2_db_task(data_col):
    with OperMysql(**mysql_testplat) as db:
        db.insert_many(data_col)


def async_res_2_db(data_col):
    t = threading.Thread(target=res_2_db_task, args=(data_col,))
    t.start()


if __name__ == "__main__":
    db_msg = {
        "host": '192.168.3.118',
        "port": 3306,
        "user": "root",
        "passwd": "Xingrui@jiatuimysql",
        "dbname": "jt_company_center"
    }
    # with OperMysql(**db_msg) as db:
    #     rows, result = db.run("select login_name,password,company_name from jt_company_center.ai_company limit 10")
    #     LogUtils.debug(rows)
    #     LogUtils.debug(result[0])

    datas = [{
        'className': 'login',
        'methodName': '/arch-login-center/corp/list',
        'description': '企管组织架构成员增删改-获取企管登陆信息',
        'rank': 1,
        'uri': '/arch-login-center/corp/list',
        'spendTime': '0.23 s',
        'status': '成功',
        'logs': ['errmsg', '---------------------....', 'error_type']
    }, {
        'className': 'test_bmsDepartmentOpera',
        'methodName': '/company-center/structure/department/delete',
        'description': '企管组织架构部门增删改-删除部门',
        'rank': 1,
        'uri': '/company-center/structure/department/delete',
        'spendTime': '0.185 s',
        'status': '失败',
        'logs': [
            "响应断言异常！'43265' != '0'\n- 43265\n+ 0\n : code断言TestCase.assertEqual失败，预期值(0) - 实际值(43265)!\n",
            "...",
            "error_type"]
    }]

    db_msg_ = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'dbname': '112_apitest_plat'
    }

    with OperMysql(**db_msg_) as db_:
        db_.insert_many(datas)
