from okcoin_spot_API import OKCoinSpot
from data_filter import global_data_filter
import datetime
import time

# 初始化api_key，secret_key,url
api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
secret_key = '7C1DDC1745C93B87BE1643A689938459'
okcoin_rest_url = 'www.okcoin.cn'

# 现货API
okcoinSpot = OKCoinSpot(okcoin_rest_url, api_key, secret_key)


def rest_ticker(symbol):
    """
    date: 返回数据时服务器时间
    buy: 买一价
    high: 最高价
    last: 最新成交价
    low: 最低价
    sell: 卖一价
    vol: 成交量(最近的24小时)
    symbol  String  否(默认btc_cny)   btc_cny:比特币    ltc_cny :莱特币
    :param symbol: 'btc_cny' 'ltc_cny' 
    :return: 
    """
    # print('现货行情 ticker: symbol=%s' % symbol)
    try:
        data = okcoinSpot.ticker(symbol)
    except Exception as e:
        print('Exception rest_ticker:', e)
        return

    # print(strftime("%H:%M:%S"), data, type(data))
    global_data_filter.rest_add_data_for_ticker(data)


def rest_depth(**kwargs):
    """
    asks :卖方深度
    bids :买方深度
    symbol  String  否(默认btc_cny)    btc_cny:比特币 ltc_cny :莱特币
    size    Integer 否(默认200)        value: 1-200
    merge   Integer 否(默认 merge参数不传时返回0.01深度)    合并深度: 1, 0.1
    :param kwargs: 
    :return: 
    """
    # symbol = kwargs['symbol'] if 'symbol' in kwargs else 'btc_cny'
    # size = kwargs['size'] if 'size' in kwargs else 200
    # merge = kwargs['merge'] if 'merge' in kwargs else ''
    # print('现货深度 depth: symbol=%s size=%s merge=%s' % (symbol, size, merge))
    try:
        data = okcoinSpot.depth(**kwargs)
    except Exception as e:
        print('Exception rest_depth:', e)
        return
    # print(okcoinSpot.depth(**kwargs))
    global_data_filter.rest_add_data_for_depth(data)


def rest_trades(**kwargs):
    """
    date:交易时间
    date_ms:交易时间(ms)
    price: 交易价格
    amount: 交易数量
    tid: 交易生成ID
    type: buy/sell
    symbol  String  否   btc_cny:比特币 ltc_cny :莱特币
    since   Long    否   tid:交易记录ID（返回数据不包括当前tid值,最多返回600条数据）
    :param kwargs: 
    :return: 
    """
    # symbol = kwargs['symbol'] if 'symbol' in kwargs else 'btc_cny'
    # since = kwargs['since'] if 'since' in kwargs else ''
    # print('现货历史交易信息 trades: symbol=%s since=%s' % (symbol, since))
    try:
        data = okcoinSpot.trades(**kwargs)
    except Exception as e:
        print('Exception rest_trades', e)
        return
    # print(okcoinSpot.trades(**kwargs))
    global_data_filter.rest_add_data_for_trades(data)
    # print('--------------------------------------------')
    # for j, d in enumerate(data):
    #     print(j, d)


def rest_kline(*, symbol, type, **kwargs):
    """
    1417536000000,	时间戳
    2370.16,	开
    2380,		高
    2352,		低
    2367.37,	收
    17259.83	交易量
    symbol  String  是   btc_cny：比特币， ltc_cny：莱特币
    type    String  是  1min : 1分钟  3min : 3分钟  5min : 5分钟  15min : 15分钟    30min : 30分钟
                        1day : 1日   3day : 3日   1week : 1周  1hour : 1小时     2hour : 2小时
                        4hour : 4小时 6hour : 6小时 12hour : 12小时
    size    Integer 否(默认全部获取)   指定获取数据的条数
    since   Long    否(默认全部获取)   时间戳（eg：1417536000000）。 返回该时间戳以后的数据
    :param symbol: 
    :param type: 
    :param kwargs: 
    :return: 
    """
    # size = kwargs['size'] if 'size' in kwargs else ''
    # since = kwargs['since'] if 'since' in kwargs else ''
    # print('现货K线数据 kline: symbol=%s type=%s size=%s since=%s' % (symbol, type, size, since))
    try:
        data = okcoinSpot.kline(symbol=symbol, type=type, **kwargs)
    except Exception as e:
        print('Exception rest_kline', e)
        return
    global_data_filter.rest_add_data_for_kline(data)
    # print(okcoinSpot.kline(symbol=symbol, type=type))
    print('-----------------------------')
    # for i, l in enumerate(data):
    #     print(i, datetime.datetime.fromtimestamp(l[0] / 1000), l)


if __name__ == '__main__':
    # for i in range(10):
    #     rest_ticker('btc_cny')
    # print(global_data_filter.get_ticker_list())

    # for i in range(1000):
    #     print(i)
    #     rest_depth(symbol='btc_cny', size=20)
    #     print(global_data_filter.get_depth_list())
    #     time.sleep(1)
    # for i in range(1000):
    #     rest_trades()
    #     for j, d in enumerate(global_data_filter.get_trades_list()):
    #         print(j, d)
    #     time.sleep(1)
    for i in range(10):
        rest_kline(symbol='btc_cny', type='1min', size=40)
        for i, d in enumerate(global_data_filter.get_kline_list()):
            print(i, datetime.datetime.fromtimestamp(d['timestamp'] / 1000), d)
