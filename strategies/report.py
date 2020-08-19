# -*-coding:utf-8-*-
import pandas as pd

import baostock as bs
from strategies import cache


# 业绩预告
@cache.memoize()
def get_forecast(code):
    """
    performanceExpPubDate 业绩预告发布日期
    performanceExpStatDate 业绩预告统计日期
    profitForcastType 业绩预告类型  例如：净利润预增
    profitForcastChgPctUp 同比增长

    :param code:
    :return:
    """
    lg = bs.login()

    rs_forecast = bs.query_forecast_report(code, start_date="2020-01-01")
    rs_forecast_list = []
    while (rs_forecast.error_code == '0') & rs_forecast.next():
        rs_forecast_list.append(rs_forecast.get_row_data())
    df = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)

    df = df[['code', 'profitForcastExpPubDate', 'profitForcastType', 'profitForcastChgPctUp']]
    df = df.rename(columns={'performanceExpPubDate': 'PubDate', 'profitForcastType': 'ForcastType',
                            'profitForcastChgPctUp': 'PctUp'})

    report = ''
    bs.logout()
    if not df.empty:
        latest = df.iloc[-1].values
        up = round(float(latest[3]), 2) if latest[3] else 0
        report = f'{latest[1]}业绩预告:{latest[2]} (增长率: {up}% )'
    return report


# 业绩快报
@cache.memoize()
def get_express(code):
    """
    performanceExpPubDate 业绩快报披露日
    performanceExpressGRYOY 业绩快报营业总收入同比
    performanceExpressOPYOY 业绩快报营业利润同比
    :param code:
    :return:
    """

    lg = bs.login()

    rs = bs.query_performance_express_report(code)
    result_list = []

    while (rs.error_code == '0') & rs.next():
        result_list.append(rs.get_row_data())

    df = pd.DataFrame(result_list, columns=rs.fields)

    bs.logout()

    df = df[['code', 'performanceExpPubDate', 'performanceExpressGRYOY', 'performanceExpressOPYOY']]
    report = ''
    if not df.empty:
        latest = df.iloc[-1].values
        gr_yoy = round(float(latest[2]), 2) if latest[3] else 0
        op_yoy = round(float(latest[3]), 2) if latest[3] else 0
        report = f'{latest[1]}快报披露: 营业总收入增长率:{gr_yoy} (营业利润增长率: {op_yoy}% )'
    return report


def add_forecast(df):
    df['forecast'] = df['symbol'].apply(lambda symbol: get_forecast(symbol))
    return df


def add_express(df):
    df['express'] = df['symbol'].apply(lambda symbol: get_express(symbol))
    return df
