#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 客户端调用，用于查看API返回结果

from okcoin_spot_API import OKCoinSpot
from time import sleep, strftime

# 初始化api_key，secret_key,url
api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
secret_key = '7C1DDC1745C93B87BE1643A689938459'
okcoin_rest_url = 'www.okcoin.cn'

# 现货API
okcoinSpot = OKCoinSpot(okcoin_rest_url, api_key, secret_key)


def test_ticker(string):
    """
    date: 返回数据时服务器时间
    buy: 买一价
    high: 最高价
    last: 最新成交价
    low: 最低价
    sell: 卖一价
    vol: 成交量(最近的24小时)
    symbol  String  否(默认btc_cny)   btc_cny:比特币    ltc_cny :莱特币
    :param string: 'btc_cny' 'ltc_cny' 
    :return: 
    """
    print(u'%s 现货行情 ' % string)
    while True:
        print(strftime("%H:%M:%S"), okcoinSpot.ticker(string))
        sleep(1)


def test_depth(**kwargs):
    """
    asks :卖方深度
    bids :买方深度
    symbol  String  否(默认btc_cny)    btc_cny:比特币 ltc_cny :莱特币
    size    Integer 否(默认200)        value: 1-200
    merge   Integer 否(默认 merge参数不传时返回0.01深度)    合并深度: 1, 0.1
    :param symbol: 
    :return: 
    """
    symbol = kwargs['symbol'] if 'symbol' in kwargs else 'btc_cny'
    size = kwargs['size'] if 'size' in kwargs else 200
    merge = kwargs['merge'] if 'merge' in kwargs else ''
    print('现货深度 depth: symbol=%s size=%s merge=%s' % (symbol, size, merge))
    print(okcoinSpot.depth(**kwargs))


# test_ticker('btc_cny')
# test_ticker('ltc_cny')
test_depth(symbol='btc_cny', size=3)

# print(u' 现货历史交易信息 ')
# print(okcoinSpot.trades())
