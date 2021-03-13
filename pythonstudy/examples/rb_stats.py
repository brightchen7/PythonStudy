#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# @File    : rb_stats.py
# @Time    : 2021/1/16 16:39
# @Author  : Bright Chen
# @Mail    : bright_chen7@163.com
# --------------------------------

import pandas as pd
from pathlib import Path
import re


def find_date(rb_path):
    return rb_path.stem[11:19]


def find_file(rb_path, *keywords):
    # 根据给定的关键字查找文件
    file_names = []
    for file in rb_path.iterdir():
        flag = True
        file_name = file.name
        for w in keywords:
            if file_name.find(w) < 0:
                flag = False
        if flag:
            if file_name[:2] != "~$":
                file_names.append(file_name)
    if len(file_names) == 0:
        print('未找到{}对应的文件'.format(keywords))
        return None
    elif len(file_names) == 1:
        return file_names[0]
    elif len(file_names) > 1:
        print('发现多个{}对应的文件'.format(keywords), file_names)
        return file_names[0]


def load_rb(rb_path, date):
    '''读取project_list所对应RiskBook中的借券记录，project_list可以以['F16','1234','918']表示'''
    # 获取RiskBooking对应的文件名称
    file_name_rb = find_file(rb_path, 'RiskBooking', date)

    df_rb = pd.read_excel(rb_path.joinpath(file_name_rb),
                          sheet_name='持仓明细',
                          header=1)
    df_rb_spot = df_rb[['标的指数', '证券代码', '当前市值']].rename(
        columns={'标的指数': 'project'}).copy()
    df_rb_future = df_rb[['项目', '合约代码', '当前市值.1']].rename(
        columns={'项目': 'project', '当前市值.1': '当前市值'}).copy()

    # 若为字符型数据，转化为int
    df_rb_spot['当前市值'] = df_rb_spot['当前市值'].apply(
        lambda x: int(x.replace(',', ''))
        if isinstance(x, str) else x)
    df_rb_future['当前市值'] = df_rb_future['当前市值'].apply(
        lambda x: int(x.replace(',', ''))
        if isinstance(x, str) else x)
    df_rb_spot.dropna(inplace=True)
    df_rb_spot.reset_index(drop=True, inplace=True)
    df_rb_future.dropna(inplace=True)
    df_rb_future.reset_index(drop=True, inplace=True)
    print('##### 完成读取RiskBooking数据 #####')
    return df_rb_spot, df_rb_future


def market_value(df_rb, proj, proj_like=None):
    if proj is not None:
        return df_rb[df_rb['project'] == proj]['当前市值'].sum()
    elif proj_like is not None:
        return df_rb[df_rb['project'].apply(
            lambda x: re.match(proj_like, x) is not None)]['当前市值'].sum()


# task1
def gen_arb_stats(df_rb):
    PB = market_value(df_rb, 'PBRISK-BLK', None) + \
        market_value(df_rb, 'PBRISK-BLK300', None)
    FT = market_value(df_rb, 'HKSL-BLK', None) + \
        market_value(df_rb, 'HKSL-BLK300', None)
    ZRT = abs(market_value(df_rb, None, '^INDEX-ARB-ZRT'))
    IA = market_value(df_rb, 'INDEX-ARB', None)
    IA_other = market_value(df_rb, None, '^INDEX-ARB-')
    IA300 = market_value(df_rb, None, '^INDEX-ARB300-')
    IA_SUMMARY = abs(IA + IA300 + IA_other)
    ELN = IA_SUMMARY - PB - FT - ZRT
    print('##### IndexArb Complete #####')
    return {
        'IndexArb': {
            'PB': format_number(PB),
            'FT': format_number(FT),
            'ELN': format_number(ELN),
            'ZRT': format_number(ZRT),
            'SUMMARY': format_number(IA_SUMMARY)}}


# task2
def zhiya(df_rb, ZRT_ls):
    PB = abs(market_value(df_rb, 'ZHIYA-PB', None))
    FT = abs(market_value(df_rb, 'ZHIYA-HKFT', None))
    ZRT = abs(sum([market_value(df_rb, zrt, None) for zrt in ZRT_ls]))
    SUMMARY = abs(market_value(df_rb[df_rb['当前市值'] < 0], None, '^ZHIYA'))
    ELN = SUMMARY - PB - FT - ZRT
    print('##### Zhiya Complete #####')
    return {
        'Zhiya': {
            'PB': format_number(PB),
            'FT': format_number(FT),
            'ELN': format_number(ELN),
            'ZRT': format_number(ZRT),
            'SUMMARY': format_number(SUMMARY)}}


# task3
def strategy(df_rb):
    edspbprop2 = market_value(df_rb[df_rb['当前市值'] < 0], None, '^EDSPBPROP2')
    edspbprop2_hk = market_value(
        df_rb[df_rb['当前市值'] < 0], 'EDSPBPROP2-HK', None)
    edspbprop2_eln = market_value(
        df_rb[df_rb['当前市值'] < 0], 'EDSPBPROP2-ELN', None)
    edspbprop2_pb = market_value(
        df_rb[df_rb['当前市值'] < 0], 'EDSPBPROP2-PB', None)
    print('##### Strategy Complete #####')
    return {
        'Stragegy': {
            'PB': format_number(edspbprop2_pb),
            'FT': format_number(edspbprop2_hk),
            'ELN': format_number(edspbprop2_eln),
            'SUMMARY': format_number(edspbprop2)}}


# task4
def future(df_rb):
    pb_mv = market_value(df_rb, 'LEND-PB', None)
    ft_mv = market_value(df_rb, 'LEND-HK', None)
    summary = ft_mv + pb_mv
    print('##### Future Complete #####')
    return {
        'Future': {
            'PB': format_number(pb_mv),
            'FT': format_number(ft_mv),
            'SUMMARY': format_number(summary)}}


# task5
def gen_sbl_stats(df_rb):
    sbl_total_mv = market_value(df_rb[df_rb['当前市值'] < 0], None, '^SBL-')
    sbl_hk_mv = market_value(df_rb[df_rb['当前市值'] < 0], None, '^SBL-.*-HK$')
    sbl_zrt_mv = market_value(df_rb[df_rb['当前市值'] < 0],
                              None,
                              '^SBL-.*-ZRT$') + market_value(df_rb[df_rb['当前市值'] < 0],
                                                             None,
                                                             '^SBL-.*-HX$')
    sbl_eln_mv = sbl_total_mv - sbl_hk_mv - sbl_zrt_mv
    print('##### ELN Complete #####')
    return {
        'SBL': {
            'ELN': format_number(sbl_eln_mv),
            'HK': format_number(sbl_hk_mv),
            'ZRT': format_number(sbl_zrt_mv),
            'SUMMARY': format_number(sbl_total_mv)}}


# task6
def lend(df_rb):
    HKSL = market_value(df_rb[df_rb['当前市值'] < 0], 'HKSL', None)
    HKSL_ = market_value(df_rb, None, '^HKSL-') - \
        market_value(df_rb, None, '^HKSL-BLK')
    FT = HKSL + HKSL_
    PBSL = market_value(df_rb, 'PBSL', None)
    PBSL_ = market_value(df_rb, None, '^PBSL-') - \
        market_value(df_rb, None, '^PBSL-BLK')
    PB = PBSL + PBSL_
    summary = FT + PB
    print('##### Lend Complete #####')
    return {'Lend': {
        'FT': format_number(FT),
        'PB': format_number(PB),
        'SUMMARY': format_number(summary)}}


def gen_result(path_txt, date, res_ls):
    def dict_to_df(res):
        KEY = list(res.keys())[0]
        df = pd.DataFrame([[date, KEY, key, value] for key, value in res[KEY].items(
        )], columns=['Date', 'Project', 'Pool', 'MV'])
        return df

    df_rb_spot, df_rb_future = load_rb(path_txt, date)

    res_ia = gen_arb_stats(df_rb_spot)
    res_zhiya = zhiya(df_rb_spot, res_ls)
    res3_strat = strategy(df_rb_spot)
    res_future = future(df_rb_future)
    res_eln = gen_sbl_stats(df_rb_spot)
    res_lend = lend(df_rb_spot)

    df = pd.DataFrame(columns=['Date', 'Project', 'Pool', 'MV'])
    for res in [res_ia, res_zhiya, res3_strat, res_future, res_eln, res_lend]:
        df = pd.concat([df, dict_to_df(res)])
    df.reset_index(drop=True)
    return df


def format_number(number):
    return "{:,.2f}".format(number)


def run_by_date(rb_path, res_ls, date, is_output=False):
    result = gen_result(rb_path, date, res_ls)
    print(result)
    if is_output:
        result.to_csv(rb_path.joinpath('stats' + date + '.csv'))


def run_all(rb_path, res_ls):
    data = pd.DataFrame()
    for file in rb_path.iterdir():
        if file.is_file() and "RiskBooking" in file.name:
            date = find_date(file)
            print(date)
            result = gen_result(rb_path, date, res_ls)
            data = data.append(result, ignore_index=True)
    data.to_csv(rb_path.joinpath('stats_all.csv'))
    # result.to_csv(rb_path.joinpath('stats' + date + '.csv'))


if __name__ == '__main__':
    run_date = '20201231'
    base_path = Path(r'E:\cicc\融券\rb_month')
    zhiya_zrt_ls = [
        'ZHIYA_GTDL-WB',
        'ZHIYA-GTDL',
        'ZHIYA_GTDL-WB',
        'ZHIYA-JDYG',
        'ZHIYA-ZRT',
        'ZHIYA-ZRTGJ']
    # run_by_date(base_path, zhiya_zrt_ls, run_date)
    run_all(base_path, zhiya_zrt_ls)
