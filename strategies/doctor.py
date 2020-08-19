# -*-coding:utf-8-*-
import os
from datetime import datetime, timedelta

import pandas as pd

from conf.configs import Config
from strategies.rps import add_rps
from strategies.report import add_forecast, add_express


# 超过一年以上
def more_than_one_years(filename):
    df = pd.read_pickle(Config.BASIC_STOCKS)
    # _now = datetime(2020,7,1)
    # than_one = (_now.date() - timedelta(weeks=52)).strftime('%Y-%m-%d')
    than_one = (datetime.now().date() - timedelta(weeks=52)).strftime('%Y-%m-%d')
    df = df[df['ipoDate'] < than_one]
    # df = df.tail(1000)
    final_df = add_rps(df)
    final_df.to_pickle(filename)
    print('rps生成数据完成')


# 基金持股3%
def fund_three_holding():
    """
    LTZB:占流通股比
    :return:
    """
    df = pd.read_pickle(Config.FUND_STOCKS)[['SCode', 'SName', 'LTZB']]
    df['LTZB'] = df['LTZB'].apply(lambda x: float(x))
    df = df[df['LTZB'] >= 3]
    final_df = df.rename(columns={'SCode': 'code', 'SName': 'name', 'LTZB': 'rate'})
    return final_df


# 北向持股超过3千万
def beixiang_thirty_million():
    """
    DateType: 日排行版
    HdDate： 日期
    SCode : 代码
    SName: 名称
    LTZB : 占流通股比
    ZZB : 占总股本
    ShareSZ : 市值
    :return:
    """
    df = pd.read_pickle(Config.BEIXIANG_STOCKS)
    df['ShareSZ'] = df['ShareSZ'].apply(lambda x: float(x))
    df = df[df['ShareSZ'] > 300000000][['SCode', 'SName', 'ShareSZ']]
    final_df = df.rename(columns={'SCode': 'code', 'SName': 'name', 'ShareSZ': 'share'})
    return final_df


def merge(filename):
    df1 = pd.read_pickle(filename)
    df2 = fund_three_holding()
    df3 = pd.merge(df1, df2, on=['name', 'code', ])
    df4 = beixiang_thirty_million()
    final_df = pd.merge(df3, df4, on=['name', 'code', ])
    # print(final_df[final_df['name']=='浪潮信息'][['name', 'code', 'rps_50', 'rps_120', 'rps_250']])
    return final_df[(final_df['rps_120'] > 90) & (final_df['rps_250'] >= 90) & (final_df['rps_50'] >= 90)]


def run():
    # 生产rps数据
    filename = datetime.now().date().strftime('%Y_%m_%d') + '_rps.pkl'
    if not os.path.exists(filename):
        more_than_one_years(filename)
    df = merge(filename)[['symbol', 'name', 'rps_50', 'rps_120', 'rps_250', 'latest_date', 'latest_price']]
    df = df.drop_duplicates()
    df = df.sort_values(by='rps_50', ascending=False, axis=0)

    df = add_forecast(df)
    df = add_express(df)
    pd.set_option('display.expand_frame_repr', False)
    print(df)
    print(df.shape)


if __name__ == '__main__':
    run()
