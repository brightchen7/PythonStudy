#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------
# @File    : path_study.py
# @Time    : 2020/2/27 22:37
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

from pathlib import Path


def basic_example():
    p = Path('.')
    print([x for x in p.iterdir() if x.is_file()])
    print(list(p.glob('**/*.py')))

    p = Path(r'D:\CodeRepo\Github\PythonStudy')
    q = p / 'pythonstudy'
    print(f'{q.absolute().name}, type{type(q.name)}')
    q = q.joinpath('buildin_function')
    print(p.exists())
    print(q)
    print(q.exists())
    if p.exists():
        print([x for x in p.iterdir() if x.is_file()])
    else:
        print(f"no path for {p.name}")
    q = q / "path_study.py"
    if q.exists():
        with q.open() as f:
            print(f.readline())
    else:
        print(f'no file for {q.name}')


def read_msg(path_txt):
    p = Path(path_txt)
    for file in p.iterdir():
        if file.is_file() & file.suffix.endswith('msg'):
            print(file.name)


# Case 1
# rename bu removing website
def rename_case(your_path):
    suffix_list = ['rmvb', 'mkv', 'mp4']
    p = Path(your_path)
    # print([x for x in p.iterdir() if x.is_file()])
    for x in p.iterdir():
        if x.is_file() and x.suffix[1:] in suffix_list:
            names = x.name.split('.')
            if 'www' in names[0]:
                new_name = '.'.join(names[3:])
                print("{} -> {}".format(x.name, new_name))
                x.replace(x.with_name(new_name))


if __name__ == '__main__':
    basic_example()
    # read_msg(r"E:\cicc\Fund\netvalue")
    # rename_case('E:\\迅雷下载')
