# -*-coding:utf-8-*-
import pandas as pd
import baostock as bs
from strategies import cache


def get_daily_trade_data(code):
    lg = bs.login()

    rs = bs.query_history_k_data_plus(code,
                                      "date,code,close,isST",
                                      start_date='2019-01-01',
                                      frequency="d",
                                      adjustflag="2")

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    bs.logout()
    return result


@cache.memoize()
def calculating_growth_rate(code='sz.000001'):
    print(f'正在处理股票: {code}')
    df = get_daily_trade_data(code)
    latest = df.iloc[-1].values
    cols = df.shape[0]
    a = float(df.iloc[-1].values[2])
    b = float(df.iloc[-50].values[2])
    c = float(df.iloc[-120].values[2])
    d = float(df.iloc[-250].values[2]) if cols >= 250 else float(df.iloc[-cols].values[2])
    rate_50 = (a - b) / b
    rate_120 = (a - c) / c
    rate_250 = (a - d) / d
    return rate_50, rate_120, rate_250, latest[0], latest[2]


def add_rps(df=None):
    df['growth_50'] = df['code'].apply(lambda code: calculating_growth_rate(code)[0])
    df['growth_120'] = df['code'].apply(lambda code: calculating_growth_rate(code)[1])
    df['growth_250'] = df['code'].apply(lambda code: calculating_growth_rate(code)[2])
    df['latest_date'] = df['code'].apply(lambda code: calculating_growth_rate(code)[3])
    df['latest_price'] = df['code'].apply(lambda code: calculating_growth_rate(code)[4])
    df['symbol'] = df['code']
    df['code'] = df['code'].apply(lambda x: x.split('.')[-1])
    # df.to_pickle('growth.pkl')
    # df = pd.read_pickle('growth.pkl')
    x = df.shape[0]  # 行数
    y = df.shape[1]  # 列数
    # 设置level_0 --> growth_20
    df = df.sort_values(by='growth_50', ascending=False, axis=0)  # 升序
    df = df.reset_index()
    df.index = df.index + 1
    df = df.reset_index(level=0)
    df['rps_50'] = (1 - df['level_0'] / x) * 100
    df = df[
        ['symbol', 'code', 'code_name', 'growth_120', 'growth_250', 'rps_50', 'ipoDate', 'latest_date', 'latest_price']]

    df = df.sort_values(by='growth_120', ascending=False, axis=0)  # 升序
    df = df.reset_index()
    df.index = df.index + 1
    df = df.reset_index(level=0)

    df['rps_120'] = (1 - df['level_0'] / x) * 100
    df = df[
        ['symbol', 'code', 'code_name', 'growth_250', 'rps_50', 'rps_120', 'ipoDate', 'latest_date', 'latest_price']]

    # 设置level_1 --> growth_50
    df = df.sort_values(by='growth_250', ascending=False, axis=0)  # 升序
    df = df.reset_index()
    df.index = df.index + 1
    df = df.reset_index()
    df['rps_250'] = (1 - df['level_0'] / x) * 100
    df = df[['symbol', 'code', 'code_name', 'rps_50', 'rps_120', 'rps_250', 'ipoDate', 'latest_date', 'latest_price']]

    final_df = df.rename(columns={'code_name': 'name', 'ipoDate': 'date'})
    return final_df


def monthly_reversal(df):
    """
    日线收盘价站上年线；
    一月内曾创50日新高
    50日的RPS大于85；
    收盘价站上年线的天数大于2，小于30；
    最高价距离120日内的最高价不到10%；
    :param df:
    :return:
    """
    condition_1 = df['rps_50'] > 85
    condition_2 = df['rps_50'] > 85
    pass


if __name__ == '__main__':
    r = calculating_growth_rate('sz.300783')
    print(r)
