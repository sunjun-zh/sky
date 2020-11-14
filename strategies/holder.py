# -*-coding:utf-8-*-

import json
from datetime import datetime

import pandas as pd

from macd.parse import Macd
from strategies.stocks import query_sz50_stocks, query_hs300_stocks, query_zz500_stocks


def _calculate_26_date():
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    return (datetime.now() + relativedelta(months=-52)).date()


def save_one_wealth_stocks():
    df1 = pd.read_pickle('one_more.pkl')
    df2 = pd.read_excel('20201114120853.xlsx', header=1)

    df = df1[df1['name'].isin(df2['名称'].values)]
    df.to_pickle('one_wealth_stocks.pkl')


def prepare_first_status(code):
    """
    入场时机 --> a状态
    :return:
    """
    df = Macd.get_monthly_data(code=code)
    print(df.tail(5))
    # df = Macd.get_daily_macd(code=code)
    the_last_one = df[-1:].to_dict('record')[0]
    second_last = df[-2:-1].to_dict('record')[0]

    third_last = df[-3:-2].to_dict('record')[0]

    last_dif = the_last_one.get('dif')
    last_dea = the_last_one.get('dea')
    last_macd = the_last_one.get('macd')
    print(f'''
    macd的数据:: 
                    dif: {last_dif}
                    dea: {last_dea}
                    macd: {last_macd}
    ''')
    second_last_dif = second_last.get('dif')
    second_last_dea = second_last.get('dea')
    second_last_macd = second_last.get('macd')
    third_last_macd = third_last.get('macd')

    # a状态 macd=(diff-dea)*2
    condition_1 = (last_macd >= 0) and (last_dif >= last_macd * 2)
    condition_2 = (third_last_macd > second_last_macd) and (second_last_macd < last_macd)
    condition_3 = (third_last_macd < second_last_macd <= 0 <= last_macd)

    return condition_1 and (condition_2 or condition_3)


def get_all_progressive_status_2(type=None):
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
    # 基金3% + 北向3000万 + 上市一年以上
    elif type == 4:
        df = pd.read_pickle('choice.pkl')
        codes = []
        for stock in df.to_dict('records'):
            code = stock['symbol']
            code_name = stock['name']
            codes.append([code, code_name])
        category = '特别加持股'
    # 北向3000万 + 上市一年以上
    elif type == 5:
        # 总数：224
        df = pd.read_pickle('smart.pkl')
        codes = []
        for stock in df.to_dict('records'):
            code = stock['symbol']
            code_name = stock['name']
            codes.append([code, code_name])
        category = '优质聪明股'
    elif type == 6:
        category = '金字塔'
        from utils.const import codes as const_codes
        from conf.configs import Config
        shares = json.load(open(Config.HOLDER_PATH, 'r'))
        codes = []
        for stock in shares:
            code_name = stock['name']
            _code = stock['code']
            a = next(filter(lambda x: x['code'] == _code, const_codes))
            code = a['fullname']
            codes.append([code, code_name])
    elif type == 7:
        # 总个数:1149  上市一年以上+市值大约100亿  
        df = pd.read_pickle('one_wealth_stocks.pkl')
        codes = []
        for stock in df.to_dict('records'):
            code = stock['symbol']
            code_name = stock['name']
            codes.append([code, code_name])
        category = '所有股票'

    else:
        print("请选择正确type值")
        return

    res = []

    for code, code_name in codes:
        print('-' * 20)
        print('现在正在处理:', code_name)
        if prepare_first_status(code):
            res.append({'code': code, 'name': code_name, 'category': category})

    with open(f'{category}(holder)({ts}).json', 'a') as f:
        f.write(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':
    # save_one_wealth_stocks()
    # df = pd.read_pickle('one_wealth_stocks.pkl')
    get_all_progressive_status_2(7)
