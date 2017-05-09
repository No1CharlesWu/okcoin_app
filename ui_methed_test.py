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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_app.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
