#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : apscheduler_study.py
# @Time    : 2021/10/6 19:13
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

'''
sample code for apscheduler
'''

from datetime import datetime
from datetime import date
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

scheduler = BlockingScheduler()

def date_job(text):
    print(text)

def tick():
    print('Tick! The time is: %s' % datetime.now())

def interval_job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))

def cron_job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))

def trigger_cron():
    scheduler = BlockingScheduler()
    # 在每天22点，每隔 1分钟 运行一次 job 方法
    scheduler.add_job(cron_job, 'cron', hour=22, minute='*/1', args=['job1'])
    # 在每天22和23点的25分，运行一次 job 方法
    scheduler.add_job(cron_job, 'cron', hour='22-23', minute='25', args=['job2'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def trigger_interval_example():
    scheduler = BlockingScheduler()
    # 每隔 1分钟 运行一次 job 方法
    scheduler.add_job(interval_job, 'interval', minutes=1, args=['job1'])
    # 在 2019-08-29 22:15:00至2019-08-29 22:17:00期间，每隔1分30秒 运行一次 job 方法
    scheduler.add_job(interval_job, 'interval', minutes=1, seconds = 30, start_date='2019-08-29 22:15:00', end_date='2019-08-29 22:17:00', args=['job2'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def trigger_date():
    scheduler = BlockingScheduler()
    # 在 2019-8-30 运行一次 job 方法
    scheduler.add_job(date_job, 'date', run_date=date(2021, 10, 6), args=['text1'])
    # 在 2019-8-30 01:00:00 运行一次 job 方法
    scheduler.add_job(date_job, 'date', run_date=datetime(2021, 10, 6, 19, 18, 0), args=['text2'])
    # 在 2019-8-30 01:00:01 运行一次 job 方法
    scheduler.add_job(date_job, 'date', run_date='2021-10-6 19:18:00', args=['text3'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def backgroud_trigger():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


# @scheduler.scheduled_job('interval', seconds=5)
# def job1():
#     t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     print('job1 --- {}'.format(t))
#
# @scheduler.scheduled_job('cron', second='*/7')
# def job2():
#     t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     print('job2 --- {}'.format(t))
# scheduler.start()

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


if __name__ == '__main__':
    # trigger_date()
    backgroud_trigger()