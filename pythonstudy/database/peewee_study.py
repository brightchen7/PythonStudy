#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
--------------------------------
@File    : peewee_study.py
@Time    : 2020/9/12 11:00
@Author  : Bright Chen
@Mail    : bright_chen7@163.com
--------------------------------
'''


from peewee import *
from datetime import date

# 连接数据库
database = MySQLDatabase(
    'test_peewee',
    user='root',
    host='localhost',
    port=3306,
    password='123456')
database.connect()

# 定义Person


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = database

# 创建表


def create():
    Person.create_table()

    # 创建表也可以这样, 可以创建多个
    # database.create_tables([Person])

# 添加一条数据


def add():
    p = Person(
        name='liuchungui',
        birthday=date(
            1990,
            12,
            20),
        is_relative=True)
    p.save()


def update():
    # 已经实例化的数据,指定了id这个primary key,则此时保存就是更新数据
    p = Person(
        name='liuchungui',
        birthday=date(
            1990,
            12,
            20),
        is_relative=False)
    p.id = 1
    p.save()

    # 更新birthday数据
    q = Person.update({Person.birthday: date(1983, 12, 21)}
                      ).where(Person.name == 'liuchungui')
    q.execute()


def query():
    # 查询单条数据
    p = Person.get(Person.name == 'liuchungui')
    print(p.name, p.birthday, p.is_relative)

    # 使用where().get()查询
    p = Person.select().where(Person.name == 'liuchungui').get()
    print(p.name, p.birthday, p.is_relative)

    # 查询多条数据
    persons = Person.select().where(Person.is_relative)
    for p in persons:
        print(p.name, p.birthday, p.is_relative)


if __name__ == '__main__':
    # add()
    #  update()
    query()
