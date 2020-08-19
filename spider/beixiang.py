# -*-coding:utf-8-*-
from datetime import datetime, timedelta
import requests

import pandas as pd
from conf.configs import Config

# 北向资金
def get_beixiang_stocks():
    cookies = {
        'cowCookie': 'true',
        'st_si': '26368078327240',
        'HAList': 'a-sh-601688-%u534E%u6CF0%u8BC1%u5238',
        'em_hq_fls': 'js',
        'waptgshowtime': '2020811',
        'qgqp_b_id': 'a6fbb1ea3180f1eaa42bbcc80df61737',
        'intellpositionL': '196px',
        'st_asi': 'delete',
        'st_pvi': '16329395883523',
        'st_sp': '2020-08-11%2008%3A27%3A04',
        'st_inirUrl': 'http%3A%2F%2Fdata.eastmoney.com%2Fdzjy%2Fdefault.html',
        'st_sn': '49',
        'st_psi': '20200811130759732-113300303605-4320939707',
        'intellpositionT': '581px',
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
        ('filter', '(DateType=\'1\' and HdDate=\'2020-08-10\')'),
        ('rt', '53237416'),
    )

    date = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    results = []
    pageIndex = 1
    pageSize = 50
    pages = 1

    while pageIndex <= pages:
        print('页面:', pageIndex)
        url = f"http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGT20_GGTJ_SUM&token=894050c76af8597a853f5b408b759f5d&st=ShareSZ_Chg_One&sr=-1&p={pageIndex}&ps={pageSize}&js=var%20oHwBgGmr={{pages:(tp),data:(x)}}&filter=(DateType=%271%27%20and%20HdDate=%27{date}%27)&rt=53237416"
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
