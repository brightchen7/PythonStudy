#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : python_mail.py
# @Time    : 2021/3/14 0:46
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

'''
simple example of python smtp
'''


import smtplib
from email.header import Header
from email.mime.text import MIMEText
# from email.utils import parseaddr, formataddr

# 163邮箱服务器地址
SMTP_SERVER = 'smtp.163.com'
# 发件人邮箱地址
FROM_ADDR = 'bright_chen7@163.com'
# 发件人邮箱密码(使用申请的客户端授权码代替)
PASSWD = 'XZJGHZXDQXCQNACI'
# 收件人邮箱地址
TO_ADDR = 'bright_chen7_hk@163.com'


def send_email(subject_str, content_txt, from_addr, to_list):
    '''
    function of send mail
    :param subject_str: mail subject
    :param content_txt: mail content
    :param from_addr: from address
    :param to_list: to address
    :return: no return
    '''
    # 获取SMTP对象
    server = smtplib.SMTP()
    server.connect(host=SMTP_SERVER, port=25)
    # 登录163邮箱服务器
    server.login(user=FROM_ADDR, password=PASSWD)
    # build content
    msg = build_content(subject_str, content_txt)
    msg['From'] = f'bright_chen7<{from_addr}>'
    msg['To'] = ";".join(to_list)
    # 发送邮件
    server.sendmail(from_addr=FROM_ADDR, to_addrs=TO_ADDR, msg=msg.as_string())
    # 退出邮箱服务器
    server.quit()
    server.close()

def build_content(subject_str, content_txt):
    '''
    build content of mail string object
    :param subject_str:  subject of mail
    :param content_txt: content of mail
    :return: None
    '''
    # 构建邮件内容(参数:邮件内容; 类型-plain,html; 编码)
    msg = MIMEText(content_txt, 'plain', 'utf-8')
    # 设置邮件主题
    msg['Subject'] = Header(subject_str, charset='utf-8')
    return msg


if __name__ == '__main__':
    send_email("life is short", "smtp mail service", FROM_ADDR, TO_ADDR)
