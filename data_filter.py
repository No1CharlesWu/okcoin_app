from collections import namedtuple
import threading
import datetime


class DataFilter(object):
    __instance = None

    def __init__(self):
        self.__ticker_list = list()
        self.__depth_list = list()
        self.__trades_list = list()
        self.__kline_list = list()
        self.lock_ticker_list = threading.Lock()
        self.lock_depth_list = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if DataFilter.__instance is None:
            DataFilter.__instance = object.__new__(cls, *args, **kwargs)
        return DataFilter.__instance

    def websocket_add_data(self, data):
        channel = data['channel']
        if 'ticker' in channel:
            t = threading.Thread(target=self.websocket_ticker_filter, name='ticker_filter', args=(data,))
            t.start()
        elif 'depth' in channel:
            d = threading.Thread(target=self.websocket_depth_filter, name='depth_filter', args=(data,))
            d.start()
        elif 'trades' in channel:
            # TODO
            # self.__trades_list.extend(data['data'])
            # self.__trades_list.sort(key=lambda l: l[0])
            pass
        elif 'kline' in channel:
            # TODO
            # self.__kline_list.extend(data['data'])
            # self.__kline_list.sort(key=lambda l: l[0])
            pass

    def websocket_ticker_filter(self, data):
        self.lock_ticker_list.acquire()
        try:
            self.__ticker_list.append(data['data'])
            print('ticker: websocket add data')
        finally:
            self.lock_ticker_list.release()

    def rest_add_data_for_ticker(self, data):
        self.lock_ticker_list.acquire()
        try:
            temp = data['ticker']
            for k, v in temp.items():
                temp[k] = float(v)
            temp['timestamp'] = int(data['date']) * 1000
            self.__ticker_list.append(temp)
            print('ticker: rest add data')
        finally:
            self.lock_ticker_list.release()

    def get_ticker_list(self):
        if len(self.__ticker_list) == 0:
            return None
        self.lock_ticker_list.acquire()
        try:
            self.__ticker_list.sort(key=lambda d: d['timestamp'])
            r_data = self.__ticker_list.pop()
            self.__ticker_list.clear()
            print('ticker: get data added.')
            return r_data
        finally:
            self.lock_ticker_list.release()

    def websocket_depth_filter(self, data):
        self.lock_depth_list.acquire()
        try:
            # print('depth: websocket add data')
            temp = data['data']
            for i, l in enumerate(temp['asks']):
                temp['asks'][i][0] = float(l[0])
                temp['asks'][i][1] = float(l[1])
            for i, l in enumerate(temp['bids']):
                temp['bids'][i][0] = float(l[0])
                temp['bids'][i][1] = float(l[1])
            # print(datetime.datetime.now(), datetime.datetime.fromtimestamp(data['data']['timestamp']/1000))
            self.__depth_list.append(temp)
            print('depth: websocket add data')
        finally:
            self.lock_depth_list.release()

    def rest_add_data_for_depth(self, data):
        self.lock_depth_list.acquire()
        try:
            data['timestamp'] = int(datetime.datetime.now().timestamp() * 1000)
            self.__depth_list.append(data)
            print('depth: rest add data')
        finally:
            self.lock_depth_list.release()

    def get_depth_list(self):
        if len(self.__depth_list) == 0:
            return None
        self.lock_depth_list.acquire()
        try:
            self.__depth_list.sort(key=lambda d: d['timestamp'])
            r_data = self.__depth_list.pop()
            self.__depth_list.clear()
            print('depth: get data added.')
            return r_data
        finally:
            self.lock_depth_list.release()

    def trades_add_data(self, data):
        # TODO
        # 交易记录应该合并才对。
        trades = namedtuple('trades', ['tid', 'price', 'amount', 'timestamp', 'type'])
        for i, d in enumerate(data):
            tmp = trades(int(d['tid']), float(d['price']), float(d['amount']), int(d['date_ms']), d['type'])
            self.__trades_list.append(tmp)

    def kline_add_data(self, data):
        # TODO
        # 根据时间段进行数据合并
        kline = namedtuple('kline', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])
        for i, l in enumerate(data):
            tmp = kline(l[0], l[1], l[2], l[3], l[4], l[5])
            self.__kline_list.append(tmp)

    def get_trades_list(self):
        return self.__trades_list

    def get_kline_list(self):
        return self.__kline_list


global_data_filter = DataFilter()
