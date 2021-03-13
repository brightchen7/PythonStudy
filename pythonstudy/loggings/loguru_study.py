#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
--------------------------------
@File    : loguru_study.py
@Time    : 2020/2/15 17:41
@Author  : Bright Chen
@Mail    : bright_chen7@163.com
--------------------------------
'''

from loguru import logger
import sys

logger.debug("That's it, beautiful and simple logging!")
one = logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.info("test new add!")
logger.remove(one)

logger.add("./log/file_{time:YYYYMMDD}.log", rotation="5 MB")
logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")

logger.add(sys.stdout, colorize=True, format="<green>%{file}</green><r>{name}:{module}:{line}</r> <level>{message}</level>")
logger.info("test color")

# @logger.catch
# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)
#
# my_function(0,0,0)