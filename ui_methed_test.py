import sys
import websocket
import okcoin_spot_API
import okcoin_websocket
import ui_app
import zlib
import json
from datetime import datetime
from time import sleep
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from data_filter import get_global_data_filter


def ui_change_status_label(self):
    self.status_label.setText('sb')


def ui_thread_websocket_start(self):
    t = threading.Thread(target=okcoin_websocket.websocket_start, name='websocket_start')
    t.start()


def display_ticker_table(self):
    last = 0
    ok = False
    while True:
        d = get_global_data_filter().get_ticker_list()
        new_time = d['timestamp']
        if new_time >= last:
            last = new_time
            ok = True
        else:
            ok = False
        print('ui', ok, new_time)
        self.ticker_table.clearContents()
        tmp = QtWidgets.QTableWidgetItem(str(d['timestamp']))
        self.ticker_table.setItem(0, 0, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['buy']))
        self.ticker_table.setItem(0, 1, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['sell']))
        self.ticker_table.setItem(0, 2, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['high']))
        self.ticker_table.setItem(0, 3, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['low']))
        self.ticker_table.setItem(0, 4, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['last']))
        self.ticker_table.setItem(0, 5, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['vol']))
        self.ticker_table.setItem(0, 6, tmp)
        self.ticker_table.update()
        sleep(0.2)


def ui_thread_display_ticker_table(self):
    t = threading.Thread(target=display_ticker_table, name='display_ticker_table', args=(self,))
    t.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_app.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
