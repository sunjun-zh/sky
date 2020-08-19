# -*-coding:utf-8-*-
from conf.configs import Config


def proxy():
    # 隧道服务器
    tunnel_host = Config.TUNNEL_HOST
    tunnel_port = Config.TUNNEL_PORT

    proxies = {
        "http": "http://%s:%s@%s:%s/" % (Config.TID, Config.TID_PWD, tunnel_host, tunnel_port),
        "https": "https://%s:%s@%s:%s/" % (Config.TID, Config.TID_PWD, tunnel_host, tunnel_port)
    }

    return proxies


def get_ua():
    import os
    import json
    import random
    from conf.configs import Config

    file_path = os.path.join(os.path.join(Config.ROOT_PATH, 'data'), 'useragent.json')
    data = random.choice(json.load(open(file_path, 'r')))
    return [v for _, v in data.items()][0]


def fake_headers(cookie=None):
    ua = get_ua()
    headers = {
        'authority': 'www.holdle.com',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': ua,
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'referer': 'https://www.holdle.com/pyramid/index',
        'cookie': cookie,
        # 'if-none-match': 'W/"b0ea0bf6341e151225197e192f3599e2"',
        'Referer': 'https://www.holdle.com/assets/application-6cc4d4956d28431ae20a39fa53db5cb41c2eaf422581ddcdba0afce644c093fe.css',
        'User-Agent': ua,
        'Origin': 'https://www.holdle.com',
    }
    return headers
