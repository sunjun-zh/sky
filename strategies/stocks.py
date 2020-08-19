# -*-coding:utf-8-*-
import baostock as bs
import pandas as pd

from conf.configs import Config


# 上证50
def query_sz50_stocks():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息

    # 获取上证50成分股
    rs = bs.query_sz50_stocks()

    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    result = pd.DataFrame(sz50_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    # result.to_csv("D:/sz50_stocks.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()
    return result


def query_hs300_stocks():
    # 登陆系统
    lg = bs.login()

    # 获取沪深300成分股
    rs = bs.query_hs300_stocks()

    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    # result.to_csv("D:/hs300_stocks.csv", encoding="gbk", index=False)
    # 登出系统
    bs.logout()
    return result


# 中证500
def query_zz500_stocks():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取中证500成分股
    rs = bs.query_zz500_stocks()

    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    # result.to_csv("D:/zz500_stocks.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()
    return result


def get_all_stock():
    """
    code 代码
    code_name 证券名称
    ipoDate 上市日期
    outDate 退市日期
    type 1 股票 2 指数 3 其他
    status 1 上市  0 退市
    :return:
    """
    lg = bs.login()
    rs = bs.query_stock_basic()
    stocks = []
    while (rs.error_code == '0') & rs.next():
        stocks.append(rs.get_row_data())
    df = pd.DataFrame(stocks, columns=rs.fields)

    #  股票+ 上市
    final_df = df[(df['type'] == '1') & (df['status'] == '1')]
    final_df.to_pickle(Config.BASIC_STOCKS)

    bs.logout()


if __name__ == '__main__':
    get_all_stock()
