from PyQt5 import QtCore, QtGui, QtWidgets
from ui_methed_test import *
import threading
import random
import datetime
import time
import data_filter


class Ui_MainWindow(object):
    ticker = {'data': {'timestamp': 0, 'buy': 0, 'sell': 0, 'high': 0, 'low': 0, 'last': 0, 'vol': 0},
              'update': {'now_time': 0, 'timestamp_update': False, 'buy_update': False, 'sell_update': False,
                         'high_update': False, 'low_update': False, 'last_update': False, 'vol_update': False},
              'send_rest': True, 'last_time': 0}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1209, 755)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(10, 30, 113, 32))
        self.connect_button.setObjectName("connect_button")
        self.ticker_table = QtWidgets.QTableWidget(self.centralwidget)
        self.ticker_table.setGeometry(QtCore.QRect(390, 10, 781, 81))
        self.ticker_table.setAutoFillBackground(False)

        self.ticker_table.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))

        self.ticker_table.setObjectName("ticker_table")
        self.ticker_table.setColumnCount(7)
        self.ticker_table.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticker_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem('asdfghjk')
        self.ticker_table.setItem(0, 0, item)
        self.status_label = QtWidgets.QLabel(self.centralwidget)

        self.status_label.setGeometry(QtCore.QRect(130, 30, 241, 31))
        self.status_label.setObjectName("status_label")

        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(20, 60, 194, 24))
        self.dateTimeEdit.setObjectName("dateTimeEdit")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1209, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.connect_button.clicked.connect(self.to_connect)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.change_time)
        self.ticker_timer = QtCore.QTimer()
        self.ticker_timer.timeout.connect(self.change_ticker_table)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_time(self):
        pass
        # dt = datetime.datetime.now()
        # self.status_label.setText(dt.strftime('%a, %b %d %H:%M:%S'))
        # self.status_label.setText(str(dt.timestamp()))
        # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # self.dateTimeEdit.setDateTime(QtCore.QDateTime.fromString(now_time, 'yyyy-MM-dd hh:mm:ss'))

    def change_ticker_table(self):
        # print(datetime.datetime.now().timestamp())
        # self.status_label.setText(str(datetime.datetime.now().timestamp()))
        print('触发时钟')
        update_ticker_table(self)

    def to_connect(self):
        self.timer.start(1000)
        self.ticker_timer.start(1000)
        ui_thread_websocket_start(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_button.setText(_translate("MainWindow", "连接"))
        item = self.ticker_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "BTC"))
        item = self.ticker_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间"))
        item = self.ticker_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "买"))
        item = self.ticker_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "卖"))
        item = self.ticker_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "最高"))
        item = self.ticker_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "最低"))
        item = self.ticker_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "最新"))
        item = self.ticker_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "成交量"))
        __sortingEnabled = self.ticker_table.isSortingEnabled()
        self.ticker_table.setSortingEnabled(False)
        self.ticker_table.setSortingEnabled(__sortingEnabled)
        self.status_label.setText(_translate("MainWindow", "状态："))
