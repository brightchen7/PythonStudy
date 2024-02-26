#!/usr/bin/env python
# coding=utf-8

import argparse
import sys

def get_cmd_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('args', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    return args.cmd, args.args

def main():
    cmd, args = get_cmd_args()
    print(cmd, args)

main()