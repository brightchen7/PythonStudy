#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
--------------------------------
@File    : get_netvalue.py
@Time    : 2020/9/13 17:31
@Author  : Bright Chen
@Mail    : bright_chen7@163.com
--------------------------------
'''

from pathlib import Path
import win32com.client
from bs4 import BeautifulSoup


def read_msg(path_txt):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    for file in Path(path_txt).iterdir():
        if file.is_file() & file.suffix.endswith('msg'):
            message = outlook.openSharedItem(str(file.absolute()))
            # print(message.Subject)
            fund_name = get_fund_name(message.Subject)
            value_date, fund_value = parse_mail(message.HTMLBody)
            print(f"Fund:{fund_name}, Date:{value_date}, Value:{fund_value}")


def parse_mail(mail_body):
    soup = BeautifulSoup(mail_body, 'lxml')
    net_value = soup.find(lambda tag: tag.name == "p" and "基金单位净值" in tag.text)
    if len(net_value) == 0:
        print("FATAL: the mail format is changed, please make a big notice")
        return None, None
    span_value = net_value.find_all('span')
    return span_value[1].text, handle_colon(span_value[4].text)


# get rid of ":" before the net value
def handle_colon(value_string):
    if value_string[0] == ":":
        return value_string[1:]
    else:
        return value_string


def get_fund_name(mail_subject):
    names = mail_subject.split(" ")
    if len(names) > 1:
        if '【请管理人确认估值表】' in names[-2]:
            return names[-2].split("】")[-1]
        else:
            return names[-2]
    else:
        print("error: can not get fund name from subject")
        return mail_subject


def test_suite():
    print(handle_colon(': 1.058'))
    print(handle_colon('1.058'))
    test_name1 = '转发: 致远私享十号私募证券投资基金产品 2020-06-04净值情况'
    print(get_fund_name(test_name1))
    test_name2 = '致远私享十号私募证券投资基金产品 2020-04-01净值情况'
    print(get_fund_name(test_name2))
    test_name3 = '答复  致远私享十三号私募证券投资基金产品 2020-04-28净值情况'
    print(get_fund_name(test_name3))
    test_name4 = '【请管理人确认估值表】朋锦红海2号私募证券投资基金产品 2020-04-10估值表'
    print(get_fund_name(test_name4))
    test_name5 = '【请以此份为准】【请管理人确认估值表】朋锦红海2号私募证券投资基金产品 2020-04-10估值表'
    print(get_fund_name(test_name5))


if __name__ == '__main__':
    read_msg(r"E:\cicc\Fund\netvalue")
