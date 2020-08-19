# -*-coding:utf-8-*-
import os
import pandas as pd

import baostock as bs
from conf.configs import Config
from utils.const import codes


def convert(code):
    _x = list(filter(lambda x: x['code'] == code, codes))
    if _x:
        return _x[0].get('fullname')
    return None




if __name__ == '__main__':
    import pandas as pd
    from conf.configs import Config

    d = pd.read_pickle(Config.BASIC_STOCKS)
    print(d)