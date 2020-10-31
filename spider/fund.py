# -*-coding:utf-8-*-
from lxml import etree
import requests
import pandas as pd

from utils.http_util import proxy
from conf.configs import Config


# 基金
cookies = {
    'cowCookie': 'true',
    'qgqp_b_id': '57f05f971076eb5979659d53006119d6',
    'st_si': '39080851249282',
    'st_asi': 'delete',
    'dRecords': '%u6CAA%u6DF1%u6E2F%u901A%u6301%u80A1%7Chttp%3A//data.eastmoney.com/hsgtcg/%2C*%u4E3B%u529B%u6570%u636E-%u5C71%u6CB3%u836F%u8F85%7Chttp%3A//data.eastmoney.com/zlsj/detail/2020-09-30-1-300452.html',
    'intellpositionL': '521px',
    'st_pvi': '82690235654609',
    'st_sp': '2020-10-18%2009%3A12%3A15',
    'st_inirUrl': 'http%3A%2F%2Fdata.eastmoney.com%2Fzlsj%2Fjj.html',
    'st_sn': '34',
    'st_psi': '20201018094546405-113300300983-6456336933',
    'intellpositionT': '638px',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://data.eastmoney.com/zlsj/jj.html',
    'Accept-Language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7',
}


def fetch(code):
    print(f'正在处理股票代码为: {code}')
    url = f'http://data.eastmoney.com/zlsj/detail/2020-09-30-0-{code}.html'
    html = None
    try:
        response = requests.get(url,
                                headers=headers,
                                proxies=proxy(),
                                cookies=cookies,
                                verify=False)
        if response.status_code == 200:
            html = response.text
    except:
        print(f'该股票({code})数据爬取有问题')
    finally:
        return _parse_html(html, code)


def _parse_html(html, code):
    val = 0
    if html:
        docs = etree.HTML(html)
        _val = docs.xpath('//*[@id="dt_2"]/tbody/tr[1]/td[6]/text()')
        try:
            val = float(_val[0]) if _val else 0
        except:
            print(f'该股票数据问题 code:{code}, _val:{_val}')
    return val


def get_fund_data():
    df = pd.read_pickle(Config.FUND_BASIC_STOCKS)
    df['rate'] = df['SCode'].apply(lambda x: fetch(x))
    df.to_pickle(Config.FUND_STOCKS)
    print('数据生产成功')


if __name__ == '__main__':
    df = pd.read_pickle(Config.FUND_STOCKS)
    print(df)
