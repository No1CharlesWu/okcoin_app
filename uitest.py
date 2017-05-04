# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uitest.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui_methed_test import *
import threading


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1209, 755)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(60, 60, 113, 32))
        self.connect.setObjectName("connect")
        self.trickertable = QtWidgets.QTableWidget(self.centralwidget)
        self.trickertable.setGeometry(QtCore.QRect(60, 140, 741, 51))
        self.trickertable.setAutoFillBackground(False)
        self.trickertable.setObjectName("trickertable")
        self.trickertable.setColumnCount(7)
        self.trickertable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.trickertable.setItem(0, 0, item)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 110, 181, 21))
        self.label.setObjectName("label")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(190, 40, 371, 71))
        self.status_label.setObjectName("status_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1209, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.connect.clicked.connect(self.to_connect)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def to_connect(self):
        ui_thread_websocket_start()
        self.change_status_label()
        self.display_ticker_table()

    def display_ticker_table(self):
        t = threading.Thread(target=ui_thread_display_ticker_table, name='display_ticker_table', args=(self,))
        t.start()

    def change_status_label(self):
        self.status_label.setText('sb')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect.setText(_translate("MainWindow", "连接"))
        item = self.trickertable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "BTC"))
        item = self.trickertable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间"))
        item = self.trickertable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "买"))
        item = self.trickertable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "卖"))
        item = self.trickertable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "最高"))
        item = self.trickertable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "最低"))
        item = self.trickertable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "最新"))
        item = self.trickertable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "成交量"))
        __sortingEnabled = self.trickertable.isSortingEnabled()
        self.trickertable.setSortingEnabled(False)
        self.trickertable.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "BTC最新行情"))
        self.status_label.setText(_translate("MainWindow", "状态："))
