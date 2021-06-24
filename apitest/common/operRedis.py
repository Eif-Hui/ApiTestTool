# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:55 上午
# @Author  : Hui
# @File    : operRedis.py

import redis

from common.logUtils import logger


class OperRedis:
    def __init__(self, config: dict):
        try:
            self.client = redis.Redis(decode_responses=True, **config)
            # LogUtils.info("redis数据库连接成功!")
        except Exception as e:
            logger.error("redis数据库连接失败!")
            print(e)

    def get(self, name, key=None):
        try:
            if key:
                return self.client.hget(name, key)
            return self.client.get(name)
        except Exception as e:
            logger.warning(f'redis未找到目标数据(name={name},key={key}): {e}')
            return ''

    def cloese(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cloese()


if __name__ == '__main__':
    redis_env = {"host": "192.168.1.121", "port": 6379, "db": 0, "password": 'zD6MovvH6XO4Hfg'}
    with OperRedis(redis_env) as op:
        print(op.get('BURROWS_TEST_CARD_ID'))
        print(op.get('BURROWS_DEMO', 'card_id'))
