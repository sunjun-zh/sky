# -*-coding:utf-8-*-
from datetime import datetime
import json

from macd.parse import Macd
from strategies.stocks import query_sz50_stocks, query_hs300_stocks, query_zz500_stocks, get_all_stock


def _compare(i, values):
    mid = len(values) // 2
    if i <= mid:
        return values[0] <= values[i] and values[i] <= values[mid]
    else:
        return values[mid] <= values[i] and values[i] <= values[-1]


def _calculate(code):
    # 计算每支股票最近七天的 日线的macd
    df = Macd.get_daily_macd(code)
    # df = Macd.get_monthly_data(code)
    if  df.empty:
        with open('error.txt', 'a') as f:
            f.write(code + '\n')
        print(f"{code}该股票解析有问题")
        return False

    df['cross'] = abs(df['dif'] - df['dea']) < 0.05
    if not df[df['cross'] == True].empty:
        print(df)

        values = df['dif'].values.tolist()
        indexes = df.index.values.tolist()
        v = df[df['cross'] == True].tail(1).index

        i = indexes.index(v)
        if _compare(i, values):
            return True
    return False


def calculate_gold_cross(type=1):
    # 上证50成分股

    ts = datetime.now().date().strftime('%Y-%m-%d')
    if type == 1:
        category = '上证50成分股'
        codes = query_sz50_stocks()[['code', 'code_name']].values.tolist()
    # 沪深300
    elif type == 2:
        category = '沪深300成分股'
        codes = query_hs300_stocks()[['code', 'code_name']].values.tolist()
    # 中证500
    elif type == 3:
        category = '中证500成分股'
        codes = query_zz500_stocks()[['code', 'code_name']].values.tolist()
    else:
        category = '所有股票'
        codes = get_all_stock()[['code', 'code_name']].values.tolist()

    res = []
    for code, code_name in codes:
        print('-' * 20)
        print('现在正在处理:', code_name)
        if _calculate(code):
            res.append({'code': code, 'name': code_name, 'category': category})

    with open(f'{category}({ts}).json', 'a') as f:
        f.write(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':
    # calculate_gold_cross()
    calculate_gold_cross(type=2)
