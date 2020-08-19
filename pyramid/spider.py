# -*-coding:utf-8-*-
import os
import json
import requests
from lxml import etree

from conf.configs import Config
from utils.http_util import fake_headers, proxy


def fetch():
    res = requests.get(Config.HOLDER_PYRAMID, headers=fake_headers(Config.HOLER_COOKIES), proxies=proxy())
    return res.text


def download(file, filename='pyramid.html'):
    with open(filename, 'w') as f:
        f.write(file)


def _parse(pyramid_html, shares, level=1):
    """
    :param level: 王牌 1 备选 2 冷板凳 3
    :return:
    """
    temp = []
    html = etree.parse(pyramid_html, etree.HTMLParser(encoding='utf-8'))
    result = html.xpath(f'/html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[{level + 1}]/a/div//text()')
    for e in result:
        s = e.strip()
        if s:
            temp.append(s)

    for index in range(0, len(temp), 2):
        name, _code = (temp[index]).split('-')
        code = _code.split(' ')[-1]
        score = temp[index + 1]
        share = dict(
            name=name,
            code=code,
            score=score,
            level=level
        )
        shares.append(share)


def parse(pyramid_html):
    """
    part-1 /html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[2]
    part-2 /html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[3]
    part-3 /html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[4]
    :param html:
    :return:
    """
    shares = []
    _parse(pyramid_html, shares, level=1)
    _parse(pyramid_html, shares, level=2)
    _parse(pyramid_html, shares, level=3)

    return shares


def run():
    pyramid_html = os.path.join(Config.DATA_PATH, 'pyramid.html')
    if not os.path.exists(pyramid_html):
        print('pyramid.html is not found, please wait a minute!')
        html = fetch()
        download(html, filename=pyramid_html)
    print('pyramid.html is exist.')

    share_path = os.path.join(Config.DATA_PATH, 'shares.json')
    if not os.path.exists(share_path):
        print('shares.json is not found, please wait a minute!')
        results = parse(pyramid_html)
        fp = open(share_path, 'w+', encoding='utf-8')
        json.dump(results, fp, ensure_ascii=False)
    print('shares.json is exist.')

if __name__ == '__main__':
    run()