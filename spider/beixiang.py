# -*-coding:utf-8-*-
from datetime import datetime, timedelta
import requests

import pandas as pd
from conf.configs import Config


# 北向资金
def get_beixiang_stocks():
    cookies = {
        'cowCookie': 'true',
        'qgqp_b_id': '57f05f971076eb5979659d53006119d6',
        'st_si': '39080851249282',
        'st_asi': 'delete',
        'intellpositionL': '901.594px',
        'intellpositionT': '1447px',
        'st_pvi': '82690235654609',
        'st_sp': '2020-10-18%2009%3A12%3A15',
        'st_inirUrl': '',
        'st_sn': '27',
        'st_psi': '20201018093430828-113300303605-3618098728',
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/hsgtcg/list.html?DateType=DateType=%275%27',
        'Accept-Language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    }

    params = (
        ('type', 'HSGT20_GGTJ_SUM'),
        ('token', '894050c76af8597a853f5b408b759f5d'),
        ('st', 'ShareSZ_Chg_One'),
        ('sr', '-1'),
        ('p', '1'),
        ('ps', '50'),
        ('js', 'var oHwBgGmr=/{pages:(tp),data:(x)/}'),
        ('filter', '(DateType=\'1\' and HdDate=\'2020-10-16\')'),
        ('rt', '53237416'),
    )

    date = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    results = []
    pageIndex = 1
    pageSize = 50
    pages = 1

    while pageIndex <= pages:
        print('页面:', pageIndex)
        url = f"http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGT20_GGTJ_SUM&token=894050c76af8597a853f5b408b759f5d&st=ShareSZ&sr=-1&p={pageIndex}&ps={pageSize}&js=var%20YDyWHbAx={{pages:(tp),data:(x)}}&filter=(DateType=%271%27%20and%20HdDate=%272020-10-16%27)&rt=53432824"
        response = requests.get(url=url,
                                headers=headers,
                                cookies=cookies,
                                verify=False)
        res = response.text
        content = res.split('=')[-1]
        pages, data = _parse_data(content)
        results += data
        pageIndex += 1

    df = pd.DataFrame(results)
    df.to_pickle(Config.BEIXIANG_STOCKS)


def _parse_data(content):
    import re
    import json
    page_regex = "pages:(\d+),"
    data_regex = "data:(.*)}"

    pages = int(re.search(page_regex, content).group(1))
    data = re.search(data_regex, content).group(1)
    return pages, json.loads(data)


if __name__ == '__main__':
    get_beixiang_stocks()
