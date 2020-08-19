# -*-coding:utf-8-*-
import os
import json

from conf.configs import Config
from macd.parse import Macd
from utils.util import convert

from cacheout import Cache

cache = Cache(maxsize=4000)
