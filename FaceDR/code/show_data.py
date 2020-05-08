# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from database import DB
from compare_face import VisitMilvus
import configparser
import os





class ShowData(object):
    def __init__(self):
        self.db = DB()
        self.milvus = VisitMilvus()
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 231)

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 750, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)

        self.btn = QtWidgets.QPushButton(Form)
        self.btn.setGeometry(QtCore.QRect(10, 200, 50, 30))
        self.btn.setObjectName("btn")
        self.btn.setText('删除')
        self.btn.clicked.connect(self.output)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "数据显示"))
        Form.setWindowIcon(QtGui.QIcon("./data/images/icon.ico"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "选择"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "ID"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "姓名"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "性别"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "出生日期"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "手机号"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "地址"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.Form = Form
        self.show_data()

    def show_data(self):
        datas = self.db.select_all()
        self.length = len(datas)
        self.tableWidget.setRowCount(self.length)
        _translate = QtCore.QCoreApplication.translate
        for col in range(self.length):
            # item = QtWidgets.QTableWidgetItem()
            # self.tableWidget.setVerticalHeaderItem(col, item)
            # item = self.tableWidget.verticalHeaderItem(col)
            # item.setText(_translate("Form", str(col)))
            data = datas[col]
            for row in range(7):
                if row == 0:
                    item = QtWidgets.QTableWidgetItem('选择我')
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                    QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.tableWidget.setItem(col,row,item)
                else:
                    item = QtWidgets.QTableWidgetItem(str(data[row-1]))
                    item.setTextAlignment(4)
                    self.tableWidget.setItem(col, row, item)

                    # item = self.tableWidget.item(col, row)
                    # item.setText(_translate("Form", str(data[row])))

    def output(self):
        for i in range(self.length):
            status = self.tableWidget.item(i,0).checkState()
            if status == 2:
                id = self.tableWidget.item(i,1).text()
                self.db.delete_data(id)
                self.milvus.delete_fromid('facetable',int(id))
                path = self.config.get('ui_event','save_path')+str(id)+'.jpg'
                if os.path.isfile(path):
                    os.remove(path)
        message_box = QtWidgets.QMessageBox
        message_box.critical(self.Form, "Info", "已删除", message_box.Yes)
        self.show_data()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ShowData()
    ui.setupUi(MainWindow)
    ui.show_data()
    MainWindow.show()
    sys.exit(app.exec_())
