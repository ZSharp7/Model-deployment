# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
# Created by: PyQt5 UI code generator 5.12.1
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets,QtGui,Qt
import sys
import cv2
from PIL import Image
import numpy as np
import time
import qtawesome

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 465)
        # 禁止拉伸窗口大小
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        MainWindow.setStyleSheet("#MainWindow{border-image:url(../data/images/desktop_bkg.jpg);}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.camera_lab = QtWidgets.QLabel(self.centralwidget)
        self.camera_lab.setGeometry(QtCore.QRect(10, 10, 340, 241))
        self.camera_lab.setStyleSheet("background-color: rgb(158, 158, 158);")
        self.camera_lab.setText("")
        self.camera_lab.setObjectName("camera_lab")
        self.camera_btn = QtWidgets.QPushButton(self.centralwidget)
        self.camera_btn.setGeometry(QtCore.QRect(10, 280, 81, 51))
        self.camera_btn.setObjectName("camera_btn")
        self.add_data_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_data_btn.setGeometry(QtCore.QRect(100, 280, 81, 51))
        self.add_data_btn.setObjectName("add_data")
        icon1 = qtawesome.icon('fa5s.camera', color='black')
        self.camera_btn.setIcon(icon1)
        self.face_lab = QtWidgets.QLabel(self.centralwidget)
        self.face_lab.setGeometry(QtCore.QRect(360, 10, 130, 130))
        self.face_lab.setStyleSheet("background-color: rgb(158, 158, 158);")
        self.face_lab.setText("")
        self.face_lab.setObjectName("face_lab")

        self.log_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.log_text.setGeometry(QtCore.QRect(190, 280, 350, 161))
        self.log_text.setObjectName("log_text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 23))
        self.menubar.setObjectName("menubar")
        self.file_m = QtWidgets.QMenu(self.menubar)
        self.file_m.setObjectName("menu")
        self.about_m = QtWidgets.QMenu(self.menubar)
        self.about_m.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.save_m = QtWidgets.QAction(MainWindow)
        self.save_m.setObjectName("action_2")
        self.show_m = QtWidgets.QAction(MainWindow)
        self.show_m.setObjectName("action_3")
        self.setting_m = QtWidgets.QAction(MainWindow)
        self.setting_m.setObjectName("action_4")
        self.file_m.addAction(self.save_m)
        self.file_m.addAction(self.show_m)
        self.file_m.addAction(self.setting_m)
        self.menubar.addAction(self.file_m.menuAction())
        self.menubar.addAction(self.about_m.menuAction())
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.info_text = QtWidgets.QPlainTextEdit(MainWindow)
        self.info_text.setGeometry(QtCore.QRect(360, 175, 161, 100))
        self.info_text.setObjectName("adress_text")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸检测器"))
        self.camera_btn.setText(_translate("MainWindow", "Start"))
        self.add_data_btn.setText(_translate("MainWindow", "Add"))
        self.file_m.setTitle(_translate("MainWindow", "文件"))
        self.about_m.setTitle(_translate("MainWindow", "关于"))
        self.save_m.setText(_translate("MainWindow", "存储图片"))
        self.show_m.setText(_translate("MainWindow", "查看数据"))
        self.setting_m.setText(_translate("MainWindow", "设置"))

    def disp_label(self, label, image):
        image = self._letterbox_image(image.copy(), (label.width(), label.height()))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(label.width(), label.height())  # 设置图片大小
        label.setPixmap(jpg_out)  # 设置图片显示

    def printf(self, mes):
        date =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_text.append("[" + date + "] " + mes)  # 在指定的区域显示提示信息
        self.cursot = self.log_text.textCursor()
        self.log_text.moveCursor(self.cursot.End)

    def _letterbox_image(self,image, size):
        '''resize image with unchanged aspect ratio using padding'''
        image = Image.fromarray(image)
        iw, ih = image.size
        w, h = size
        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = image.resize((nw, nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128, 128, 128))
        new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))

        return np.array(new_image)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())