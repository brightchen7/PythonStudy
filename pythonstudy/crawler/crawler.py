#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
--------------------------------
@File    : crawler.py
@Time    : 2020/7/5 2:03
@Author  : Bright Chen
@Mail    : bright_chen7@163.com
--------------------------------
'''

import requests
import traceback

class Crawler(object):
    """
    采集类
    """

    def __init__(self, base_url):
        self._base_url = base_url
        self._cookie = None
        self._getCookie()

    def _getCookie(self):
        """
        获取站点cookie
        :return:
        """
        try:
            res = requests.get(self._base_url)
            res.raise_for_status()
            # TODO response.cookies获取到的是一个cookiejar对象，需要使用requests.utils.dict_from_cookiejar来
            # TODO 将cookiejar对象转换为一个字典，这个字典后续使用的时候，在请求时直接传入就可以了，
            # 如 requests.get(url, cookies=cookies)
            self._cookie = requests.utils.dict_from_cookiejar(res.cookies)
            print
            self._cookie
        except Exception as e:
            print
            e

    def get_html_text(self, url, **kwargs):
        """
        爬取网页的通用代码框架
        :param url:
        :param method:
        :param kwargs:
        :return:
        """
        try:
            kwargs.setdefault('cookies', self._cookie)
            res = requests.get(url, **kwargs)
            # TODO 若响应状态码不是200, 抛出 HTTPError 异常
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            # print requests.utils.dict_from_cookiejar(res.cookies)
            return res.text
        except Exception as e:
            print(traceback.print_exc())
            return