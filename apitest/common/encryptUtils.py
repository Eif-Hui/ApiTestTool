# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 8:53 AM
# @Author  : Hui
# @File    : encryptUtils.py

import hashlib
from common.logUtils import logger


class EncrptUtils:

    @classmethod
    def sha256(cls,data):
        h = hashlib.sha256(data.encode('utf8')).hexdigest()
        return h

    @classmethod
    def sign_for_open(cls, req_data, app_key):
        """
            加密规则要求 ：
                1、jsonBody 参数按 ASCII 码规则排序
                2、按 ${key}=${value} 方式 结合 "&"做拼接，需要注意排除values值为 Null 或"Null"的数据
                3、最后对拼接结果进行sha256加密
        """
        data = ["{}={}".format(k, v) for k, v in req_data.items() if v or v in (0, [], ())]
        data = "&".join(sorted(data)) + app_key     # 签名内容为 requestData + AppKey
        data = data.replace(" ", "")
        data = data.replace("\'", "\"")
        data = data.replace("False", "false")
        data = data.replace("True"," true")
        logger.debug(data)
        return cls.sha256(data)


if __name__ == "__main__":
    # _l = []
    # l = ["{}={}".format(k, v) for k, v in demo.items() if v or v == 0]
    # for k,v in demo.items():
    #     if v or v == 0:
    #         _l.append("{_key}={_value}".format(_key=k, _value=v))
    # print(_l)
    # print(l)

    # appKey = "ba47ffafb56a4450bdeceb67c2b56e08"
    # data = {
    #         "companyId": 201903070001,
    #         "sortList": [{
    #             "classifyId": "557532416290328576",
    #             "sortOrder": 645
    #           }, {
    #             "classifyId": "557532416764284928",
    #             "sortOrder": 1066
    #           }],
    #           "requestedAppId": "JC47ada12614801000",
    #           "accessToken": "3b7a2f11377b480e855abed4e2d14692"
    #         }
    # LogUtils.debug(EncrptUtils.sign_for_open(data, appKey))
    # "sign": "82a88bee1c3f7d8dd5354206f7959e984a30e26bda05fb3a2b1d1ae328d13e48"

    appKey = "6eaa333dd6c5425b86f5c13c5721f995"
    data = {
        "requestedAppId": "JC2854d0b0fbc15000",
        "accessToken": "ddeb3bcf5b1a42c08707030670efa8ee",
        "cardIds": [585880310260994048],
    }
    logger.debug(EncrptUtils.sign_for_open(data, appKey))
