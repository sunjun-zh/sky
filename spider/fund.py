# -*-coding:utf-8-*-
import requests

import pandas as pd

from conf.configs import Config


# 基金公司持股
def get_fund_more_three_stocks():
    cookies = {
        'cowCookie': 'true',
        'st_si': '26368078327240',
        'intellpositionL': '1152px',
        'HAList': 'a-sh-601688-%u534E%u6CF0%u8BC1%u5238',
        'em_hq_fls': 'js',
        'waptgshowtime': '2020811',
        'qgqp_b_id': 'a6fbb1ea3180f1eaa42bbcc80df61737',
        'dRecords': '%u5927%u5B97%u4EA4%u6613%7Chttp%3A//data.eastmoney.com/dzjy/default.html%2C*%u5927%u5B97%u4EA4%u6613-%u4F0A%u5229%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/dzjy/detail/600887.html%2C*%u9AD8%u7BA1%u6301%u80A1-%u4F0A%u5229%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/executive/600887.html%2C*%u6CAA%u6DF1A%u80A1%u516C%u544A%7Chttp%3A//data.eastmoney.com/notices/',
        'st_asi': 'delete',
        'st_pvi': '16329395883523',
        'st_sp': '2020-08-11%2008%3A27%3A04',
        'st_inirUrl': 'http%3A%2F%2Fdata.eastmoney.com%2Fdzjy%2Fdefault.html',
        'st_sn': '37',
        'st_psi': '2020081112210954-113300300982-8901927647',
        'intellpositionT': '708px',
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/zlsj/jj.html',
        'Accept-Language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    }

    results = []
    pageIndex = 1
    pageSize = 50
    pages = 1

    while pageIndex <= pages:
        url = f"http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p={pageIndex}&ps={pageSize}&jsObj=jUCPCzOI&stat=1&cmd=1&date=2020-06-30&rt=53237322"
        response = requests.get(url=url,
                                headers=headers,
                                cookies=cookies,
                                verify=False)

        res = response.text
        content = res.split(' = ')[-1]
        pages, data = _parse_data(content)
        results += data
        pageIndex += 1
    df = pd.DataFrame(results)
    df.to_pickle(Config.FUND_STOCKS)


def _parse_data(content):
    import re
    import json
    page_regex = "pages:(\d+),"
    data_regex = "data:(.*),"

    pages = int(re.search(page_regex, content).group(1))
    data = re.search(data_regex, content).group(1)
    return pages, json.loads(data)


if __name__ == '__main__':
    get_fund_more_three_stocks()
