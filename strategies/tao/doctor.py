# -*-coding:utf-8-*-
import os
from datetime import datetime, timedelta

import pandas as pd

from conf.configs import Config
from strategies.tao.rps import add_rps
from strategies.report import add_forecast, add_express


# 超过一年以上
def more_than_one_years():
    df = pd.read_pickle(Config.BASIC_STOCKS)
    than_one = (datetime.now().date() - timedelta(weeks=52)).strftime('%Y-%m-%d')
    df = df[df['ipoDate'] < than_one]
    final_df = df.rename(columns={'code_name': 'name', 'ipoDate': 'date', 'code': 'symbol'})
    final_df['code'] = final_df['symbol'].apply(lambda x: x.split('.')[-1])
    return final_df


# 基金持股3%
def fund_three_holding():
    """
    rate: 占总股本比例(%)
    :return:
    """
    df = pd.read_pickle(Config.FUND_STOCKS)
    df = df[df['rate'] >= 3]
    final_df = df.rename(columns={'SCode': 'code', 'SName': 'name'})
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
    df['ShareSZ'] = df['ShareSZ'].apply(lambda x: round(float(x) / 100000000, 2))
    df = df[df['ShareSZ'] > 3][['SCode', 'SName', 'ShareSZ']]
    final_df = df.rename(columns={'SCode': 'code', 'SName': 'name', 'ShareSZ': 'share'})
    return final_df


def choice_stocks():
    """
    date>1year & fund>3% & bei >3000w
    :return:
    """
    df1 = more_than_one_years()
    df2 = fund_three_holding()
    df3 = pd.merge(df1, df2, on=['name', 'code', ])
    df4 = beixiang_thirty_million()
    choice = pd.merge(df3, df4, on=['name', 'code', ])
    choice.to_pickle('choice.pkl')

def smart_stocks():
    df2 = fund_three_holding()
    df4 = beixiang_thirty_million()
    smart = pd.merge(df2, df4, on=['name', 'code', ])
    smart.to_pickle('smart.pkl')


def run():
    if not os.path.exists('choice.pkl'):
        choice_stocks()
    df = pd.read_pickle('choice.pkl')

    # 生产rps数据
    filename = datetime.now().date().strftime('%Y_%m_%d') + '_rps.pkl'
    # filename = '2020_08_20' + '_rps.pkl'
    if not os.path.exists(filename):
        df = add_rps(df)
        df.to_pickle(filename)
    df = pd.read_pickle(filename)
    df = df.drop_duplicates()

    if not os.path.exists('final.pkl'):
        df = add_forecast(df)
        df = add_express(df)
        df.to_pickle('final.pkl')
    final_df = pd.read_pickle('final.pkl')
    pd.set_option('display.expand_frame_repr', False)
    final_df['forecast_rate'] = final_df['forecast_rate'].apply(lambda x: float(x) if x else 0)

    print(final_df[final_df['name'] == '宁德时代'])

    # final_df = final_df[(final_df['rps_250'] >= 80) & (final_df['rps_50'] >= 80)]
    final_df = final_df[final_df['rps_50'] >= 80]
    final_df = final_df.sort_values(by='forecast_date', ascending=False, axis=0)

    print(final_df)
    print(final_df.shape)


if __name__ == '__main__':
    # run()
    df = more_than_one_years()
    print(df)
    # df.to_pickle('one_more.pkl')


