import sys
import websocket
import okcoin_spot_API
import okcoin_websocket
import uitest
import zlib
import json
from datetime import datetime
from time import sleep
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from data_filter import get_global_data_filter


def ui_thread_websocket_start():
    t = threading.Thread(target=okcoin_websocket.websocket_start, name='websocket_start')
    t.start()


def ui_thread_display_ticker_table(self):
    while True:
        d = get_global_data_filter().get_ticker_list()
        print('ui', d)
        tmp = QtWidgets.QTableWidgetItem(str(d['timestamp']))
        self.trickertable.setItem(0, 0, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['buy']))
        self.trickertable.setItem(0, 1, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['sell']))
        self.trickertable.setItem(0, 2, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['high']))
        self.trickertable.setItem(0, 3, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['low']))
        self.trickertable.setItem(0, 4, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['last']))
        self.trickertable.setItem(0, 5, tmp)
        tmp = QtWidgets.QTableWidgetItem(str(d['vol']))
        self.trickertable.setItem(0, 6, tmp)
        self.trickertable.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = uitest.Ui_MainWindow()
    ui.setupUi(MainWindow)
    new = QtWidgets.QTableWidgetItem('1000')
    ui.trickertable.setItem(0, 1, new)
    MainWindow.show()
    sys.exit(app.exec_())
