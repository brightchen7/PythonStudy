#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
--------------------------------
@File    : arrow_intro.py
@Time    : 2020/3/7 19:43
@Author  : Bright Chen
@Mail    : bright_chen7@163.com
--------------------------------
'''

# 参考文档： https://arrow.readthedocs.io/en/latest/

import arrow

# 获取当前的时间
time_now = arrow.now()
print(time_now)
# 获取当前时间的时间戳
time_stamp = arrow.now().timestamp
print(time_stamp)
# 格式化时间
time_stamp = arrow.now().format()
print(time_stamp)
# 把字符串时间，datetime对象或时间戳转换成arrow对象
time_stamp = arrow.get(1578039096).to('local')
time_stamp2 = arrow.get("2020-01-03 16:11:36")
print(time_stamp.format("YYYY-MM-DD HH:mm:ss"))
print(time_stamp2.format("YYYY-MM-DD HH:mm:ss"))
# 替换，加减时间
arw = arrow.utcnow()
print(arw)
print(arw.replace(hour=4, minute=40))
print(arw.shift(weeks=-3))