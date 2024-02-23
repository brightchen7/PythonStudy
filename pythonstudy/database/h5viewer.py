#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName   :h5viewer.py
# @Time       :2022/8/30 18:02
# @Author     :chenl

import h5py
import numpy as np

fname = 'E:/ricequant_level2/h5/20210802.order_books.XSHE.h5'

def h5list(f,tab):
    print(tab,'Group:',f.name,'len:%d'%len(f))
    mysp2=tab[:-1]+ '  |-*'
    for vv in f.attrs.keys():  # 打印属性
        print(mysp2,end=' ')
        print('%s = %s'% (vv,f.attrs[vv]))
    mysp=tab[:-1] + '  |-'
    for k in f.keys():
        d = f[k]
        if isinstance(d,h5py.Group):
            h5list(d,mysp)
        elif isinstance(d,h5py.Dataset):
            print(mysp,'Dataset:',d.name,'(size:%d)'%d.size)
            mysp1=mysp[:-1]+ '  |-'
            print(mysp1,'(dtype=%s)'%d.dtype)
            if d.dtype.names is not None:
                print(mysp,end=' ')
                for vv in d.dtype.names:
                    print(vv,end=',')
                print()
            mysp2=mysp1[:-1]+ '  |-*'
            for vv in d.attrs.keys():  # 打印属性
                print(mysp2,end=' ')
                try:
                    print('%s = %s'% (vv,d.attrs[vv]))
                except TypeError as e:
                    print('%s = %s'% (vv,e))
                except:
                    print('%s = ?? Other ERR'% (vv,))
            #print(d[:12])  # 打印12组数据看看
        else:
            print('??->',d,'Unkown Object!')

f = h5py.File(fname,'r')
h5list(f,'')
f.close()