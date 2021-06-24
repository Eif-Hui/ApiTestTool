# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:55 上午
# @Author  : Hui
# @File    : operFileUtils.py

import configparser
from common.logUtils import logger
from config.constans import *

'''
文件操作工具类
'''


class OperFileUtils:

    @classmethod
    def read_ini(cls, filepath):
        conf = configparser.ConfigParser()  # 生成conf对象
        conf.read(filepath, encoding="utf-8-sig")
        return conf

    @classmethod
    def read_data(cls, conf, env):
        data = dict()
        try:
            data['HOST'] = conf.get('env_%s' % env, 'HOST')
            data['PORT'] = conf.get('env_%s' % env, 'PORT')
            data['USER'] = conf.get('env_%s' % env, 'USER')
            data['PASSWD'] = conf.get('env_%s' % env, 'PASSWD')
            data['DBNAME'] = conf.get('env_%s' % env, 'DBNAME')
            data['host_url'] = conf.get('env_%s' % env, 'host_url')
        except Exception as e:
            logger.debug("env %s  环境配置选项不存在" % env)
        finally:
            return data

    @classmethod
    def delete_oldest_file(cls, rm_dir, num):
        """
        保留最近num份文件
        :param rm_dir: 文件目录
        :param num: 需要保留的文件数
        :return:
        """
        files_list = os.listdir(rm_dir)
        file_dict = dict()
        for i in files_list:
            all_path = os.path.join(rm_dir, i)
            ctime = os.path.getctime(all_path)
            file_dict[all_path] = ctime
        all_path_ctime_list = sorted(file_dict.items(), key=lambda item: item[1])  # 排序
        if len(all_path_ctime_list) <= num:
            pass
        else:
            for i in range(len(all_path_ctime_list) - num):   # 删除指定文件
                os.remove(all_path_ctime_list[i][0])


if __name__ == "__main__":
    rm = root_path + "/reports/scanSwaggers/"
    OperFileUtils.delete_oldest_file(rm, 6)
