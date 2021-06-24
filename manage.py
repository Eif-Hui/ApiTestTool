# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pytest
from config.constans import *


def pytest_run():
    xml_report_path = REPORT_PATH + "/xml"
    html_report_path = REPORT_PATH + "/html"
    pytest.main([
        # '--reruns', '3',
        # '--reruns-delay', '5',
        '-s', '-v',
        '--alluredir', xml_report_path,
        '--clean-alluredir'
    ])
    cmd = f'allure generate {xml_report_path} -o {html_report_path} -c {html_report_path}'
    os.popen(cmd).read().strip()  # 运行终端命令


# Press the green button in the gutter to run the script.44
if __name__ == '__main__':
    pytest_run()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
