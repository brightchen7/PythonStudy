#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : blinker_study.py
# @Time    : 2021/10/23 23:46
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

'''
demo for studying blinker
'''

from blinker import signal
from blinker import Signal


def animal(args):
    """
    信号的接受者以及处理的逻辑代码

    :param args:
    :return:
    """
    print(f"我是小钻风，大王回来了，我要去巡山。Signal Name：{args}")


def animal_one(args):
    """
    信号的接受者以及处理的逻辑代码

    :param args:
    :return:
    """
    print(f"我是小钻风，今天的口号是: {args}")


def animal_two(args):
    """
    信号的接受者以及处理的逻辑代码

    :param args:
    :return:
    """
    print(f"我是大钻风，今天的口号是: {args}")


def animal_bro(args):
    """
    信号的接受者以及处理的逻辑代码

    :param args:
    :return:
    """
    print(f"我是小钻风，{args} 是我大哥")


def define_signal():
    """
    命名信号的例子

    :return:
    """
    # 定义一个信号
    my_signal = signal("king")
    # 信号注册一个接收者
    my_signal.connect(animal)
    # 发送信号
    my_signal.send(my_signal.name)


def anonymous_signal():
    """
    匿名信号的例子

    :return: no return
    """
    # 定义一个信号
    animal_signal = Signal()
    # 信号注册一个接收者
    animal_signal.connect(animal)
    # 发送信号
    animal_signal.send("anonymous")


def broadcast_signal():
    '''
    广播多个信号

    :return:
    '''
    k2_signal = signal("king2")
    k2_signal.connect(animal_one)
    k2_signal.connect(animal_two)
    k2_signal.send("大王叫我来巡山，抓个和尚做晚餐！")


def subsribe_signal():
    '''
    订阅信号

    :return:
    '''
    k3_signal = signal("king3")
    k3_signal.connect(animal_bro, sender="大象")
    for i in ["狮子", "大象", "大鹏"]:
        k3_signal.send(i)


if __name__ == "__main__":
    define_signal()
    anonymous_signal()
    broadcast_signal()
    subsribe_signal()
