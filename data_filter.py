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
        self.lock_trades_list = threading.Lock()
        self.lock_kline_list = threading.Lock()

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
            tr = threading.Thread(target=self.websocket_trades_filter, name='trades_filter', args=(data,))
            tr.start()
        elif 'kline' in channel:
            k = threading.Thread(target=self.websocket_kline_filter, name='kline_filter', args=(data,))
            k.start()

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
            print('ticker: get data.')
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
            # return {'asks':[],'bids':[],'timestamp':0}
            return None
        self.lock_depth_list.acquire()
        try:
            self.__depth_list.sort(key=lambda d: d['timestamp'])
            r_data = self.__depth_list.pop()
            self.__depth_list.clear()
            print('depth: get data.')
            return r_data
        finally:
            self.lock_depth_list.release()

    def websocket_trades_filter(self, data):
        t_data = data['data']
        date = str(datetime.datetime.now().date())
        self.lock_trades_list.acquire()
        try:
            for i, l in enumerate(t_data):
                temp = dict()
                temp['tid'] = int(l[0])
                temp['price'] = float(l[1])
                temp['amount'] = float(l[2])
                t_date = date + ' ' + l[3]
                temp['timestamp'] = int(datetime.datetime.strptime(t_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
                temp['type'] = l[4]
                # print(i, temp)
                if temp not in self.__trades_list:
                    self.__trades_list.append(temp)
            # for j, d in enumerate(self.__trades_list):
            #     print(j, d)
            print('trades: websocket add data')
        finally:
            self.lock_trades_list.release()

    def rest_add_data_for_trades(self, data):
        self.lock_trades_list.acquire()
        try:
            # print('rest_add_data_for_trades:', self.__trades_list)
            self.__trades_list.clear()
            for i, d in enumerate(data):
                temp = dict()
                temp['tid'] = d['tid']
                temp['price'] = float(d['price'])
                temp['amount'] = float(d['amount'])
                temp['timestamp'] = d['date_ms']
                temp['type'] = 'bid' if d['type'] == 'buy' else 'ask'
                self.__trades_list.append(temp)
                # print(i, temp)
            print('trades: rest add data')
            # for j, d in enumerate(self.__trades_list):
            #     print(j, d)
        finally:
            self.lock_trades_list.release()

    def get_trades_list(self):
        if len(self.__trades_list) == 0:
            return []
        self.lock_trades_list.acquire()
        try:
            # print(self.__trades_list, type(self.__trades_list))
            self.__trades_list.sort(key=lambda t: t['timestamp'], reverse=True)
            print('trades: get data.')
            self.__trades_list = self.__trades_list[:60]
            return self.__trades_list
        finally:
            self.lock_trades_list.release()

    def websocket_kline_filter(self, data):
        t_data = data['data']
        self.lock_kline_list.acquire()
        try:
            for i, l in enumerate(t_data):
                temp = dict()
                temp['timestamp'] = int(l[0])
                temp['open'] = float(l[1])
                temp['high'] = float(l[2])
                temp['low'] = float(l[3])
                temp['close'] = float(l[4])
                temp['vol'] = float(l[5])
                for j, d in enumerate(self.__kline_list[::]):
                    if temp['timestamp'] == d['timestamp']:
                        self.__kline_list.pop(i)
                        break
                self.__kline_list.append(temp)
            print('kline: websocket add data')
        finally:
            self.lock_kline_list.release()

    def rest_add_data_for_kline(self, data):
        self.lock_kline_list.acquire()
        try:
            self.__kline_list.clear()
            for i, l in enumerate(data):
                temp = dict()
                temp['timestamp'] = l[0]
                temp['open'] = l[1]
                temp['high'] = l[2]
                temp['low'] = l[3]
                temp['close'] = l[4]
                temp['vol'] = l[5]
                self.__kline_list.append(temp)
            print('kline: rest add data')
        finally:
            self.lock_kline_list.release()

    def get_kline_list(self):
        if len(self.__kline_list) == 0:
            return []
        self.lock_kline_list.acquire()
        try:
            self.__kline_list.sort(key=lambda k:k['timestamp'], reverse=True)
            print('trades: get data.')
            self.__kline_list = self.__kline_list[:40]
            return self.__kline_list
        finally:
            self.lock_kline_list.release()


global_data_filter = DataFilter()
