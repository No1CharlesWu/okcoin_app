import sys
import websocket
import okcoin_spot_API
import okcoin_websocket
import ui_app
import zlib
import json
import datetime
from time import sleep
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from data_filter import global_data_filter
import okcoin_rest
import random
import copy


def ui_change_status_label(self):
    pass


def ui_thread_websocket_start(self):
    t = threading.Thread(target=okcoin_websocket.websocket_start, name='websocket_start')
    t.start()


def ui_change_ticker_table(self):
    t_timestamp = self.ticker_table.itemAt(0, 0)
    t_buy = self.ticker_table.itemAt(0, 1)
    t_sell = self.ticker_table.itemAt(0, 2)
    t_high = self.ticker_table.itemAt(0, 3)
    t_low = self.ticker_table.itemAt(0, 4)
    t_last = self.ticker_table.itemAt(0, 5)
    t_vol = self.ticker_table.itemAt(0, 6)

    interval = datetime.datetime.now().timestamp() - self.ticker['update']['now_time']
    if self.ticker['update']['timestamp_update'] and interval < 1:
        t_timestamp.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_timestamp.setForeground(QtGui.QColor(255, 0, 0))
    time = self.ticker['data']['timestamp'] / 1000
    t_timestamp.setText(datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S'))
    tmp0 = QtWidgets.QTableWidgetItem(t_timestamp)

    if self.ticker['update']['buy_update'] and interval < 1:
        t_buy.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_buy.setForeground(QtGui.QColor(255, 0, 0))
    t_buy.setText('%.2f' % self.ticker['data']['buy'])
    tmp1 = QtWidgets.QTableWidgetItem(t_buy)

    if self.ticker['update']['sell_update'] and interval < 1:
        t_sell.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_sell.setForeground(QtGui.QColor(255, 0, 0))
    t_sell.setText('%.2f' % self.ticker['data']['sell'])
    tmp2 = QtWidgets.QTableWidgetItem(t_sell)

    if self.ticker['update']['high_update'] and interval < 1:
        t_high.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_high.setForeground(QtGui.QColor(255, 0, 0))
    t_high.setText('%.2f' % self.ticker['data']['high'])
    tmp3 = QtWidgets.QTableWidgetItem(t_high)

    if self.ticker['update']['low_update'] and interval < 1:
        t_low.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_low.setForeground(QtGui.QColor(255, 0, 0))
    t_low.setText('%.2f' % self.ticker['data']['low'])
    tmp4 = QtWidgets.QTableWidgetItem(t_low)

    if self.ticker['update']['last_update'] and interval < 1:
        t_last.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_last.setForeground(QtGui.QColor(255, 0, 0))
    t_last.setText('%.2f' % self.ticker['data']['last'])
    tmp5 = QtWidgets.QTableWidgetItem(t_last)

    if self.ticker['update']['vol_update'] and interval < 1:
        t_vol.setForeground(QtGui.QColor(0, 255, 0))
    else:
        t_vol.setForeground(QtGui.QColor(255, 0, 0))
    t_vol.setText('%.5f' % self.ticker['data']['vol'])
    tmp6 = QtWidgets.QTableWidgetItem(t_vol)

    self.ticker_table.clearContents()
    self.ticker_table.setItem(0, 0, tmp0)
    self.ticker_table.setItem(0, 1, tmp1)
    self.ticker_table.setItem(0, 2, tmp2)
    self.ticker_table.setItem(0, 3, tmp3)
    self.ticker_table.setItem(0, 4, tmp4)
    self.ticker_table.setItem(0, 5, tmp5)
    self.ticker_table.setItem(0, 6, tmp6)
    self.ticker_table.update()


def update_ticker_time(self, new):
    temp = self.ticker['data']
    d = dict()
    d['now_time'] = datetime.datetime.now().timestamp()
    d['timestamp_update'] = (temp['timestamp'] != new['timestamp'])
    d['buy_update'] = (temp['buy'] != new['buy'])
    d['sell_update'] = (temp['sell'] != new['sell'])
    d['high_update'] = (temp['high'] != new['high'])
    d['low_update'] = (temp['low'] != new['low'])
    d['last_update'] = (temp['last'] != new['last'])
    d['vol_update'] = (temp['vol'] != new['vol'])
    self.ticker['update'] = d
    self.ticker['data'] = new


def update_ticker_table(self):
    get_ticker = global_data_filter.get_ticker_list()
    update_ticker_time(self, self.ticker['data'])
    if get_ticker:
        self.ticker['last_time'] = datetime.datetime.now().timestamp()
        self.ticker['send_rest'] = True
        if get_ticker['timestamp'] > self.ticker['data']['timestamp']:
            update_ticker_time(self, get_ticker)
    elif self.ticker['send_rest'] and datetime.datetime.now().timestamp() - self.ticker['last_time'] > 1:
        # print('ticker_list empty. send rest.')
        ui_thread_rest_ticker(self)
        self.ticker['send_rest'] = False
    else:
        pass
        # print('等着~', self.ticker['send_rest'])
    ui_change_ticker_table(self)


def ui_thread_rest_ticker(self):
    t = threading.Thread(target=okcoin_rest.rest_ticker, name='rest_ticker', args=('btc_cny',))
    t.start()


def ui_thread_rest_depth(self):
    d = threading.Thread(target=okcoin_rest.rest_depth, name='rest_depth', kwargs={'symbol': 'btc_cny', 'since': 60})
    d.start()


def ui_thread_rest_trades(self):
    tr = threading.Thread(target=okcoin_rest.rest_trades, name='rest_trades')
    tr.start()


def ui_thread_rest_kline(self):
    k = threading.Thread(target=okcoin_rest.rest_kline, name='rest_kline',
                         kwargs={'symbol': 'btc_cny', 'type': '1min', 'size': 40})
    k.start()


def ui_change_depth_table(self):
    now_time = datetime.datetime.now().timestamp() * 1000
    self.depth_table_1.clearContents()
    self.depth_table_2.clearContents()

    for i, d in enumerate(self.depth['bids']):
        item0 = QtWidgets.QTableWidgetItem('%10.2f' % d['l'][0])
        item1 = QtWidgets.QTableWidgetItem('%9.3f' % d['l'][1])
        if now_time - d['timestamp'] <= 1000:
            item0.setForeground(QtGui.QColor(0, 255, 0))
            item1.setForeground(QtGui.QColor(0, 255, 0))
        else:
            item0.setForeground(QtGui.QColor(255, 0, 0))
            item1.setForeground(QtGui.QColor(255, 0, 0))
        if i < 20:
            self.depth_table_1.setItem(i, 0, item0)
            self.depth_table_1.setItem(i, 1, item1)
        elif i < 40:
            self.depth_table_2.setItem(i - 20, 0, item0)
            self.depth_table_2.setItem(i - 20, 1, item1)
        else:
            break

    for i, d in enumerate(self.depth['asks'][::-1]):
        item0 = QtWidgets.QTableWidgetItem('%10.2f' % d['l'][0])
        item1 = QtWidgets.QTableWidgetItem('%9.3f' % d['l'][1])
        if now_time - d['timestamp'] <= 1000:
            item0.setForeground(QtGui.QColor(0, 255, 0))
            item1.setForeground(QtGui.QColor(0, 255, 0))
        else:
            item0.setForeground(QtGui.QColor(255, 0, 0))
            item1.setForeground(QtGui.QColor(255, 0, 0))
        if i < 20:
            self.depth_table_1.setItem(i, 2, item0)
            self.depth_table_1.setItem(i, 3, item1)
        elif i < 40:
            self.depth_table_2.setItem(i - 20, 2, item0)
            self.depth_table_2.setItem(i - 20, 3, item1)
        else:
            break
    self.depth_table_1.update()
    self.depth_table_2.update()


def ui_change_trades_table(self):
    now_time = datetime.datetime.now().timestamp() * 1000
    self.trades_table_1.clearContents()
    self.trades_table_2.clearContents()

    for i, d in enumerate(self.trades['data']):
        time = d['timestamp'] / 1000
        item0 = QtWidgets.QTableWidgetItem(datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S'))
        item1 = QtWidgets.QTableWidgetItem('%d' % d['tid'])
        item2 = QtWidgets.QTableWidgetItem('%10.2f' % d['price'])
        item3 = QtWidgets.QTableWidgetItem('%9.3f' % d['amount'])
        item4 = QtWidgets.QTableWidgetItem('买入') if d['type'] == 'bid' else QtWidgets.QTableWidgetItem('卖出')
        if now_time - d['timestamp'] <= 2000:  # 本应该为1秒的。但我感觉网络延迟，就加一秒
            item0.setForeground(QtGui.QColor(0, 255, 0))
            item1.setForeground(QtGui.QColor(0, 255, 0))
            item2.setForeground(QtGui.QColor(0, 255, 0))
            item3.setForeground(QtGui.QColor(0, 255, 0))
            item4.setForeground(QtGui.QColor(0, 255, 0))
        else:
            item0.setForeground(QtGui.QColor(255, 0, 0))
            item1.setForeground(QtGui.QColor(255, 0, 0))
            item2.setForeground(QtGui.QColor(255, 0, 0))
            item3.setForeground(QtGui.QColor(255, 0, 0))
            item4.setForeground(QtGui.QColor(255, 0, 0))
        if i < 20:
            self.trades_table_1.setItem(i, 0, item0)
            self.trades_table_1.setItem(i, 1, item1)
            self.trades_table_1.setItem(i, 2, item2)
            self.trades_table_1.setItem(i, 3, item3)
            self.trades_table_1.setItem(i, 4, item4)
        elif i < 40:
            self.trades_table_2.setItem(i - 20, 0, item0)
            self.trades_table_2.setItem(i - 20, 1, item1)
            self.trades_table_2.setItem(i - 20, 2, item2)
            self.trades_table_2.setItem(i - 20, 3, item3)
            self.trades_table_2.setItem(i - 20, 4, item4)
        else:
            break

    self.trades_table_1.update()
    self.trades_table_2.update()


def ui_change_kline_table(self):
    now_time = datetime.datetime.now().timestamp() * 1000
    self.kline_table.clearContents()

    for i, d in enumerate(self.kline['data']):
        time = d['timestamp'] / 1000
        item0 = QtWidgets.QTableWidgetItem(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
        item1 = QtWidgets.QTableWidgetItem('%10.2f' % d['open'])
        item2 = QtWidgets.QTableWidgetItem('%10.2f' % d['high'])
        item3 = QtWidgets.QTableWidgetItem('%10.2f' % d['low'])
        item4 = QtWidgets.QTableWidgetItem('%10.2f' % d['close'])
        item5 = QtWidgets.QTableWidgetItem('%9.3f' % d['vol'])
        if i == 0 and self.kline['update']:  # 本应该为1秒的。但我感觉网络延迟，就加一秒
            item0.setForeground(QtGui.QColor(0, 255, 0))
            item1.setForeground(QtGui.QColor(0, 255, 0))
            item2.setForeground(QtGui.QColor(0, 255, 0))
            item3.setForeground(QtGui.QColor(0, 255, 0))
            item4.setForeground(QtGui.QColor(0, 255, 0))
            item5.setForeground(QtGui.QColor(0, 255, 0))
        else:
            item0.setForeground(QtGui.QColor(255, 0, 0))
            item1.setForeground(QtGui.QColor(255, 0, 0))
            item2.setForeground(QtGui.QColor(255, 0, 0))
            item3.setForeground(QtGui.QColor(255, 0, 0))
            item4.setForeground(QtGui.QColor(255, 0, 0))
            item5.setForeground(QtGui.QColor(255, 0, 0))
        if i < 40:
            self.kline_table.setItem(i, 0, item0)
            self.kline_table.setItem(i, 1, item1)
            self.kline_table.setItem(i, 2, item2)
            self.kline_table.setItem(i, 3, item3)
            self.kline_table.setItem(i, 4, item4)
            self.kline_table.setItem(i, 5, item5)
        else:
            break

    self.kline_table.update()


def update_depth_table(self):
    get_depth = global_data_filter.get_depth_list()
    # print(get_depth)
    if get_depth:
        update_depth_time(self, get_depth)
        self.depth['now_time'] = datetime.datetime.now().timestamp() * 1000
        self.depth['send_rest'] = True
    else:
        if datetime.datetime.now().timestamp() * 1000 - self.depth['now_time'] >= 1000 and self.depth['send_rest']:
            ui_thread_rest_depth(self)
            self.depth['send_rest'] = True
        self.depth['now_time'] = datetime.datetime.now().timestamp() * 1000
    # print('aaaaa', self.depth)
    ui_change_depth_table(self)


def update_depth_time(self, new):
    temp = list()
    for i, l in enumerate(new['asks']):
        t_d = dict()
        t_d['l'] = l
        for j, d in enumerate(self.depth['asks']):
            if l == d['l']:
                t_d['timestamp'] = d['timestamp']
                break
        else:
            t_d['timestamp'] = new['timestamp']
        temp.append(t_d)
    self.depth['asks'] = temp
    temp = list()
    for i, l in enumerate(new['bids']):
        t_d = dict()
        t_d['l'] = l
        for j, d in enumerate(self.depth['bids']):
            if l == d['l']:
                t_d['timestamp'] = d['timestamp']
                break
        else:
            t_d['timestamp'] = new['timestamp']
        temp.append(t_d)
    self.depth['bids'] = temp


def update_trades_time(self, new):
    self.trades['data'] = copy.copy(new)


def update_kline_time(self, new):
    if new[0] != self.kline['data'][0]:
        self.kline['update'] = True
    self.kline['data'] = copy.deepcopy(new)


def update_trades_table(self):
    get_trades = global_data_filter.get_trades_list()
    if get_trades:
        update_trades_time(self, get_trades)
        self.trades['now_time'] = datetime.datetime.now().timestamp() * 1000
        self.trades['send_rest'] = True
    else:
        if datetime.datetime.now().timestamp() * 1000 - self.trades['now_time'] >= 1000 and self.trades['send_rest']:
            ui_thread_rest_trades(self)
            self.trades['send_rest'] = True
        self.trades['now_time'] = datetime.datetime.now().timestamp() * 1000
    ui_change_trades_table(self)


def update_kline_table(self):
    get_kline = global_data_filter.get_kline_list()

    self.kline['update'] = False
    if get_kline:
        update_kline_time(self, get_kline)
        self.kline['now_time'] = datetime.datetime.now().timestamp() * 1000
        self.kline['send_rest'] = True
    else:
        if datetime.datetime.now().timestamp() * 1000 - self.kline['now_time'] >= 1000 and self.kline['send_rest']:
            ui_thread_rest_kline(self)
            self.kline['send_rest'] = True
        self.kline['now_time'] = datetime.datetime.now().timestamp() * 1000
    ui_change_kline_table(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_app.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
