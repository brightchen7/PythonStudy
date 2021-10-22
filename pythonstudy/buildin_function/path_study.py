#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# --------------------------------
# @File    : path_study.py
# @Time    : 2020/2/27 22:37
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------
"""

from pathlib import Path


def basic_example():
    """
    basic example of pathlib
    """
    my_path = Path(".")
    print([x for x in my_path.iterdir() if x.is_file()])
    print(list(my_path.glob("**/*.py")))

    my_path = Path(r"D:\CodeRepo\Github\PythonStudy")
    my_folder = my_path / "pythonstudy"
    my_folder = my_folder.joinpath("buildin_function")
    print(my_folder)
    print(my_folder.exists())
    print([x for x in my_path.iterdir() if x.is_file()])
    my_folder = my_folder / "path_study.py"
    with my_folder.open(encoding="utf8") as py_file:
        print(py_file.readline())


def read_msg(path_txt):
    """
    read msg file using path library
    :param path_txt: path for message file
    """
    mail_path = Path(path_txt)
    for file in mail_path.iterdir():
        if file.is_file() & file.suffix.endswith("msg"):
            print(file.name)


# Case 1
# rename bu removing website
def rename_case(your_path):
    """
    rename download file of thunder
    :param your_path: path for rename file
    """
    suffix_list = ["rmvb", "mkv", "mp4"]
    movie_path = Path(your_path)
    # print([x for x in p.iterdir() if x.is_file()])
    for movie_file in movie_path.iterdir():
        if movie_file.is_file() and movie_file.suffix[1:] in suffix_list:
            names = movie_file.name.split(".")
            if "www" in names[0]:
                new_name = ".".join(names[3:])
                print(f"{movie_file.name} -> {new_name}")
                movie_file.replace(movie_file.with_name(new_name))


if __name__ == "__main__":
    basic_example()
    # read_msg(r"E:\cicc\Fund\netvalue")
    # rename_case('E:\\迅雷下载')
