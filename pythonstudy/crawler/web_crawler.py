#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : web_crawler.py
# @Time    : 2020/7/4 18:26
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------
#

# 携带请求头参数访问知乎:
import requests
from bs4 import BeautifulSoup
import re


def get_content():
    # 请求头字典
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }

    url = "https://www.993dy.com/vod-detail-id-27433.html"
    # url = "https://www.zhihu.com/explore"
    # 在get请求内，添加user-agent
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    print(response.status_code)  # 200
    print(response.text)
    with open('hdxzd.html', 'w', encoding='utf-8') as f:
        f.write(response.text)


def parse_html():
    with open('hdxzd.html', 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        # data = soup.find_all('ul', class_ = 'downurl')
        pattern = re.compile(r"var downurls = '*';$", re.MULTILINE)
        data = soup.find("script", text=pattern)
        # print(type(data[0]))
        print(data)


parse_html()
