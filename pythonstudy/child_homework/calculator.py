#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : calculator.py
# @Time    : 2021/10/3 12:18
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

'''
program for generating my son's home work
'''


import random


def get_sub_string(sum_value, count):
    '''
    返回指定个数(count)的计算题，以计算某数(sum_value)以内的加法
    :param sum_value: 指定某数以内(的加法)
    :param count: 随机生成多少题
    :return: 返回count个计算题
    '''

    questions = ''
    count_temp = 0  # 计数器
    while True:
        first_add = random.randrange(1, sum_value)  # 随机生成 第一个加数
        result = random.randrange(2, sum_value + 1)  # 随机生成 和
        second_add = result - first_add  # 第二个加数
        if second_add > 0:
            str_temp = str(first_add) + ' + ' + str(second_add) + '' + ' = \n'
            questions += str_temp
            count_temp += 1
            if count_temp >= count:
                break
    return questions

def get_sub_list(sub_value, count):
    '''
    返回指定个数(count)的计算题，以计算某数(sum_value)以内的加法
    :param sum_value: 指定某数以内(的加法)
    :param count: 随机生成多少题
    :return: 返回count个计算题
    '''

    questions = ''
    count_temp = 0  # 计数器
    while True:
        first_sub = random.randrange(1, sub_value)  # 随机生成 第一个加数
        result = random.randrange(2, sub_value + 1)  # 随机生成 和
        second_sub = first_sub - result  # 第二个加数
        if second_sub > 0:
            str_temp = str(first_sub) + ' - ' + str(second_sub) + '' + ' = \n'
            questions += str_temp
            count_temp += 1
            if count_temp >= count:
                break
    return questions

def main():
    '''
    main function
    '''
    sum_value, count = 10, 15 # 随机出30题，10以内的加法
    final_result = get_sub_string(sum_value, count)
    final_result += get_sub_list(sum_value, count)
    str_title = f'{sum_value}以内加法算术题{count}题.doc'
    with open(str_title, "w", encoding='utf8') as doc_output:
        doc_output.write(final_result)
    doc_output.close()

if __name__ == '__main__':
    main()
