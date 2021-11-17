#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : blinker_study.py
# @Time    : 2021/10/23 23:46
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------


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
    print(f'我是小钻风，今天的口号是: {args}')


def animal_two(args):
    print(f'我是大钻风，今天的口号是: {args}')


def animal_bro(args):
    print(f'我是小钻风，{args} 是我大哥')


def define_signal():
    """
    命名信号的例子
    :return:
    """
    # 定义一个信号
    s = signal("king")
    # 信号注册一个接收者
    s.connect(animal)
    # 发送信号
    s.send(s.name)


def anonymous_signal():
    """
    匿名信号的例子
    :return:
    """
    # 定义一个信号
    s = Signal()
    # 信号注册一个接收者
    s.connect(animal)
    # 发送信号
    s.send('anonymous')


def broadcast_signal():
    s = signal('king2')
    s.connect(animal_one)
    s.connect(animal_two)
    s.send('大王叫我来巡山，抓个和尚做晚餐！')


def subsribe_signal():
    s = signal('king3')
    s.connect(animal_bro, sender='大象')
    for i in ['狮子', '大象', '大鹏']:
        s.send(i)


if "__main__" == __name__:
    define_signal()
    anonymous_signal()
    broadcast_signal()
    subsribe_signal()
