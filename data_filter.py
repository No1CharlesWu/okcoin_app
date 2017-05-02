from collections import namedtuple


class DataFilter(object):
    def __init__(self):
        self.__ticker_list = list()
        self.__depth_list = list()
        self.__trades_list = list()
        self.__kline_list = list()

    def websocket_filter_data(self, data):
        channel = data['channel']
        print(channel)
        if 'ticker' in channel:
            self.__ticker_list.append(data['data'])
            self.__ticker_list.sort(key=lambda d: d['timestamp'])
        elif 'depth' in channel:
            self.__depth_list.append(data['data'])
        elif 'trades' in channel:
            self.__trades_list.extend(data['data'])
            self.__trades_list.sort(key=lambda l: l[0])
        elif 'kline' in channel:
            self.__kline_list.extend(data['data'])
            self.__kline_list.sort(key=lambda l: l[0])

    def add_data(self, data, interface):
        if interface == 'websocket':
            self.websocket_filter_data(data)

    def ticker_add_data(self, data):
        ticker = namedtuple('ticker', ['timestamp', 'buy', 'sell', 'high', 'low', 'last', 'vol'])
        tmp = data['ticker']
        t = ticker(data['date'], float(tmp['buy']), float(tmp['sell']), float(tmp['high']), float(tmp['low']),
                   float(tmp['last']), float(tmp['vol']))
        self.__ticker_list.append(t)

    def depth_add_data(self, data):
        pass

    def trades_add_data(self, data):
        pass

    def kline_add_data(self, data):
        pass

    def get_ticker_list(self):
        return self.__ticker_list

    def get_depth_list(self):
        return self.__depth_list

    def get_trades_list(self):
        return self.__trades_list

    def get_kline_list(self):
        return self.__kline_list
