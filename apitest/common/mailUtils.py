# # -*- coding: utf-8 -*-
# # @Time    : 2021/6/20 7:55 上午
# # @Author  : Hui
# # @File    : mailUtils.py
#
# import smtplib
# import threading
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email import encoders
#
# from flask import Flask, render_template
#
# from src import app
# from utils.operFileUtils import OperFileUtils
# from common.logUtils import logger
# # from tornado.template import *
# from conf.setting import mailSwitch
# from utils.constant import email_report_template, secury_file_path, setting_file_path, template_dir
#
# """
#     发送邮件工具类
# """
#
#
# class MailUtils:
#     """
#         mailUtils = MailUtils(response)
#         root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根路径
#         root_path = root_dir[:root_dir.find("automationAPITest") + len("automationAPITest")]
#         file_path = [root_path + '/' + 'logs' + '/' + 'run.logs']
#         file_name = [u"运行时日志"]
#         mailUtils.send_main(file_path,file_name)
#     """
#
#     def __init__(self, res_dict):
#         """
#         初始化并读取配置
#         :param run_prj:
#         """
#         self.res_dict = res_dict
#         self.run_proj = res_dict['runProj']
#
#         self.mail_switch = True if mailSwitch == 'on' else False
#
#         _secury = OperFileUtils.read_ini(secury_file_path)
#         if self.mail_switch:
#             # 发送邮件(html，文本，附件)
#             self.mail_server = _secury.get('email-conf', 'smtp_server')
#             self.mail_sender = _secury.get('email-conf', 'sender')
#             self.mail_pwd = _secury.get('email-conf', 'password')
#             self.user = "InterfaceTester" + "<" + self.mail_sender + ">"  # 发件人命名
#             try:
#                 self.mail_receiver = _secury.get('reciever-conf', 'reciever_%s' % self.run_proj)
#             except Exception:
#                 self.mail_receiver = _secury.get('reciever-conf', 'reciever_demo')
#                 logger.debug('收件人配置不存在,发送邮件给默认收件人')
#
#     def _send_mail(self, type, content, subject, attachment_file=None, file_name=None):
#         """
#         发送邮件主方法
#         :param type:指定类型 text or html
#         :param content: 内容
#         :param subject: 主题
#         :param attachment_file: 附件 无则不填
#         :param file_name: 附件名 无则不填
#         :return:
#         """
#         if self.mail_switch is not True:
#             logger.debug("邮件发送功能关闭，停止发送邮件")
#             return
#         mime = 'html' if type == 'html' else 'plain'
#         message_root = MIMEMultipart()
#         message_root['From'] = self.user
#         message_root['To'] = self.mail_receiver
#         message_root['Subject'] = subject
#         message_root['Cc'] = self.mail_sender
#         message = MIMEText(content, mime, 'utf-8')
#         message_root.attach(message)
#
#         if attachment_file is not None and len(attachment_file) == len(file_name):
#             for index in range(len(attachment_file)):
#                 att = self.add_file(file_name[index], attachment_file[index])
#                 message_root.attach(att)
#         elif attachment_file is not None and len(attachment_file) != len(file_name):
#             raise Exception("ERROR PARAMS attachment_file OR file_name")
#
#         try:
#             smtp_Obj = smtplib.SMTP()
#             smtp_Obj.connect(self.mail_server, 25)  # 25 为 SMTP 端口号
#             smtp_Obj.login(self.mail_sender, self.mail_pwd)
#             smtp_Obj.sendmail(self.user, self.mail_receiver.split(";"), message_root.as_string())
#             smtp_Obj.close()
#             logger.debug("邮件发送成功")
#         except smtplib.SMTPException as e:
#             print(e)
#             logger.debug("ERROR 邮件发送失败！")
#
#     def add_file(self, file_name, file_path):
#         """
#         增加附件
#         :param file_name: 附件在邮件中显示的名称
#         :param file_path: 附件路径
#         :return:
#         """
#         attachment_file = open(file_path, 'rb').read()
#         att = MIMEBase('application', 'octet-stream')  # 构造MIMEText对象做为邮件显示内容并附加到根容器
#         att.set_payload(attachment_file)
#         att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', '接口测试报告.html'))
#         encoders.encode_base64(att)
#         return att
#
#     def send_main(self, report_file_path=None, report_name=None):
#         """
#         发送邮件执行入口
#         """
#         # tonator 模版写法
#         # loader = Loader(root_path)
#         # content = loader.load(email_report_template).generate(res=self.res_dict)
#
#         # flask + jinja2模版
#         with app.app_context():
#             content = render_template(email_report_template, res=self.res_dict)
#         sub = self.run_proj + u'接口测试报告'
#
#         # 异步发送
#         thr = threading.Thread(target=self._send_mail, name='SendMailThread', args=['html', content, sub, report_file_path, [report_name]])
#         thr.start()
#
#         # 同步发送
#         # self._send_mail('html', content, sub, report_file_path, [report_name])
#
#
# if __name__ == "__main__":
#     response = {
#         "testPass": 0,
#         "testFailedResult": [
#             {
#                 'className': 'Events',
#                 'project': "api_demo",
#                 'methodName': 'addEvent_1',
#                 'description': '添加成功',
#                 'spendTime': '0.001 s',
#                 'status': '失败',
#                 'rank': "2",
#                 "errorLevel1": 0,
#                 "errorLevel2": 1,
#                 "errorLevel3": 2,
#                 'testFail': 10
#             },
#             {
#                 'className': 'Events-2',
#                 'project': "api_demo",
#                 'methodName': 'addEvent_2',
#                 'description': '添加失败1',
#                 'spendTime': '0.001 s',
#                 'status': '失败',
#                 'rank': "2",
#                 "errorLevel1": 0,
#                 "errorLevel2": 1,
#                 "errorLevel3": 2,
#                 'testFail': 10
#             },
#             {
#                 'className': 'Events—3',
#                 'methodName': 'addEvent_3',
#                 'project': "api_demo",
#                 'description': '添加失败2',
#                 'spendTime': '0.001 s',
#                 'status': '成功',
#                 'rank': "2",
#                 "errorLevel1": 0,
#                 "errorLevel2": 1,
#                 "errorLevel3": 2,
#                 'testFail': 10
#             }
#         ],
#         "testName": "ddd",
#         "testAll": 2,
#         "testFail": 2,
#         "beginTime": "2019-06-21",
#         "totalTime": "2.0s",
#         "testSkip": 0,
#         "errorLevel1": 0,
#         "errorLevel2": 1,
#         "errorLevel3": 2,
#         "runProj": "api_demo",
#         "apiCounts": 30,
#         "passRate": "50%"
#     }
#     mailUtils = MailUtils(response)
#     mailUtils.send_main()
