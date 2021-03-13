#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : yaml_demo.py
# @Time    : 2020/8/31 16:17
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

import yaml
import os


def demo1(ymal_path):
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况。
    f = open(ymal_path, 'r', encoding='utf-8')

    cont = f.read()

    x = yaml.safe_load(cont)
    print(type(x))
    print(x)
    print(x['name'])
    print(type(x['name']))
    print(x.get('name'))
    # print(x['EMAIL']['Smtp_Server'])
    # print(type(x['EMAIL']['Smtp_Server']))
    # print(x['DB'])
    # print(x['DB']['host'])
    #
    # print(x.get('DB').get('host'))
    #
    # print(type(x.get('DB')))

# 单个文档


def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("***获取yam文件数据***")
    file = open(yaml_file, 'r', encoding='utf-8')
    file_data = file.read()
    file.close()

    print(file_data)
    print("类型", type(file_data))

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.safe_load(file_data)  # safe_load，safe_load,unsafe_load
    print(data)
    print("类型", type(data))
    return data


# yaml文件中含多个文档时，分别获取文档中数据
def get_yaml_load_all(yaml_file):
    # 打开文件
    file = open(yaml_file, 'r', encoding='utf-8')
    file_data = file.read()
    file.close()

    all_data = yaml.load_all(file_data, Loader=yaml.FullLoader)
    for data in all_data:
        print('data-----', data)


# 生成yaml文档
def generate_yaml_doc(yaml_file):
    py_ob = {"school": "zhang",
             "students": ['a', 'b']}
    file = open(yaml_file, 'w', encoding='utf-8')
    yaml.dump(py_ob, file)
    file.close()


if __name__ == '__main__':
    # 获取当前文件路径 D:/WorkSpace/StudyPractice/Python_Yaml/YamlStudy
    filePath = os.path.dirname(__file__)
    print(filePath)
    # 获取当前文件的Realpath
    # D:\WorkSpace\StudyPractice\Python_Yaml\YamlStudy\YamlDemo.py
    fileNamePath = os.path.split(os.path.realpath(__file__))[0]
    print(fileNamePath)
    # 获取配置文件的路径 D:/WorkSpace/StudyPractice/Python_Yaml/YamlStudy\config.yaml
    yaml_path = os.path.join(filePath, 'config.yaml')
    print(yaml_path)
    demo1(yaml_path)

    yaml_all_path = os.path.join(filePath, 'configall.yaml')
    get_yaml_load_all(yaml_all_path)

    # print('--------------------', yaml_path)
    # get_yaml_data(yaml_path)
