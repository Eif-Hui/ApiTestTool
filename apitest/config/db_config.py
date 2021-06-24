# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:58 上午
# @Author  : Hui
# @File    : db_config.py

# mysql
mysql_118 = {
    "host": '192.168.3.118',
    "port": 3306,
    "user": "root",
    "passwd": "Xingrui@jiatuimysql",
    "dbname": "jt_company_center"
}

mysql_testplat = {
    "host": '192.168.3.119',
    "port": 3306,
    "user": "root",
    "passwd": "Xingrui@DCDB123",
    "dbname": "112_apitest_plat"
}

mysql_119 = {
    "host": '192.168.3.119',
    "port": 3306,
    "user": "root",
    "passwd": "Xingrui@DCDB123",
    "dbname": "jt_company_center"
}

# mongodb
mongodb_120 = {
    "host": '192.168.3.120',
    "port": 27017,
    "username": 'admin',
    "password": 'admin',
    "db_name": "test"
}

# redis
redis_121 = {"host": "192.168.1.121", "port": 6379, "db": 0, "password": 'zD6MovvH6XO4Hfg'}

# db_连接器
db_connector = {
    'mysql': {
        '192.168.3.118': mysql_118,
        '192.168.3.119': mysql_119
    },
    'mongodb': {
        '192.168.3.120': mongodb_120
    },
    'redis': {
        '192.168.3.121': redis_121
    }
}
