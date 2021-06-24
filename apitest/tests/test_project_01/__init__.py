
import os
import faker
from common import operMysql
# 公共变量


current_module_path = os.path.dirname(__file__)
yaml_dir = current_module_path + '/data/'
case_dir = current_module_path + '/test_case/'

# 数据库配置
db_msg = {
    "host": '192.168.3.118',
    "port": 3306,
    "user": "root",
    "passwd": "Xingrui@jiatuimysql",
    "dbname": "jt_company_center"
}

TEST_HOST = 'https://test-daas.deepexi.com'
