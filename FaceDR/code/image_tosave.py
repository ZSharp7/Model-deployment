# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import cv2
import numpy as np
from PIL import Image
from compare_face import VisitMilvus
from database import DB
import threading
import configparser

class FromImageSave(object):
    def __init__(self, delect,facenet):
        self.delect = delect
        self.facenet = facenet
        self.face_flag = False
        self.milvus = VisitMilvus()
        self.db = DB()
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(349, 408)
        self.image_lab = QtWidgets.QLabel(Form)
        self.image_lab.setGeometry(QtCore.QRect(10, 10, 121, 121))
        self.image_lab.setStyleSheet("background-color: rgb(188, 188, 188);")
        self.image_lab.setText("")
        self.image_lab.setObjectName("image_lab")
        self.face_lab = QtWidgets.QLabel(Form)
        self.face_lab.setGeometry(QtCore.QRect(230, 20, 101, 101))
        self.face_lab.setStyleSheet("background-color: rgb(188, 188, 188);")
        self.face_lab.setText("")
        self.face_lab.setObjectName("face_lab")
        self.open_btn = QtWidgets.QPushButton(Form)
        self.open_btn.setGeometry(QtCore.QRect(90, 365, 71, 31))
        self.open_btn.setObjectName("open_btn")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.setGeometry(QtCore.QRect(180, 365, 71, 31))
        self.save_btn.setObjectName("save_btn")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 60, 91, 16))
        self.label.setStyleSheet("border-color: rgb(71, 71, 71);")
        self.label.setObjectName("label")

        self.id_lab = QtWidgets.QLabel(Form)
        self.id_lab.setGeometry(QtCore.QRect(100, 145, 31, 21))
        self.id_lab.setObjectName("id_lab")

        self.name_lab = QtWidgets.QLabel(Form)
        self.name_lab.setGeometry(QtCore.QRect(100, 180, 54, 21))
        self.name_lab.setObjectName("name_lab")

        self.sex_lab = QtWidgets.QLabel(Form)
        self.sex_lab.setGeometry(QtCore.QRect(100, 200, 41, 31))
        self.sex_lab.setObjectName("sex_lab")

        self.born_lab = QtWidgets.QLabel(Form)
        self.born_lab.setGeometry(QtCore.QRect(100, 230, 61, 21))
        self.born_lab.setObjectName("born_lab")

        self.phone_lab = QtWidgets.QLabel(Form)
        self.phone_lab.setGeometry(QtCore.QRect(100, 260, 54, 21))
        self.phone_lab.setObjectName("phone_lab")

        self.adress_lab = QtWidgets.QLabel(Form)
        self.adress_lab.setGeometry(QtCore.QRect(100, 280, 51, 31))
        self.adress_lab.setObjectName("adress_lab")



        self.id_text = QtWidgets.QLineEdit(Form)
        self.id_text.setEnabled(False)
        self.id_text.setGeometry(QtCore.QRect(170, 145, 81, 21))
        self.id_text.setObjectName("id_text")

        self.name_text = QtWidgets.QLineEdit(Form)
        self.name_text.setGeometry(QtCore.QRect(170, 180, 81, 21))
        self.name_text.setMaxLength(3)
        self.name_text.setObjectName("name_text")
        self.man_radio = QtWidgets.QRadioButton(Form)
        self.man_radio.setGeometry(QtCore.QRect(170, 200, 51, 31))
        self.man_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.man_radio.setChecked(True)
        self.man_radio.setObjectName("radioButton")
        self.women_radio = QtWidgets.QRadioButton(Form)
        self.women_radio.setGeometry(QtCore.QRect(220, 200, 51, 31))
        self.women_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.women_radio.setChecked(False)
        self.women_radio.setObjectName("radioButton_2")
        self.born = QtWidgets.QDateEdit(Form)
        self.born.setGeometry(QtCore.QRect(170, 230, 81, 21))
        self.born.setObjectName("dateEdit")
        self.phone_text = QtWidgets.QLineEdit(Form)
        self.phone_text.setGeometry(QtCore.QRect(170, 260, 113, 21))
        self.phone_text.setMaxLength(11)
        self.phone_text.setObjectName("phone_text")
        self.adress_text = QtWidgets.QPlainTextEdit(Form)
        self.adress_text.setGeometry(QtCore.QRect(170, 290, 161, 71))
        self.adress_text.setObjectName("adress_text")
        self.open_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(self.save)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.Form = Form


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.open_btn.setText(_translate("Form", "打开图片"))
        self.save_btn.setText(_translate("Form", "保存"))
        self.label.setText(_translate("Form", "检测到脸部 =》"))

        self.name_lab.setText(_translate("Form", "姓名："))
        self.sex_lab.setText(_translate("Form", "性别："))
        self.born_lab.setText(_translate("Form", "出生日期："))
        self.phone_lab.setText(_translate("Form", "手机号："))
        self.adress_lab.setText(_translate("Form", "地址："))
        self.id_lab.setText(_translate("Form", "Id:"))
        self.man_radio.setText(_translate("Form", "男"))
        self.women_radio.setText(_translate("Form", "女"))

    def open_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(None,"选择文件",os.getcwd(),'Image Files(*.jpg)')
        if os.path.isfile(directory[0]):
            self.open_btn.setEnabled(False)
            image = cv2.imread(directory[0])
            self.disp_label(self.image_lab,image)
            threading.Thread(target=self.face_thread,args=(image,)).start()
        else:
            self.disp_error('文件打开错误')

    def face_thread(self,image):
        bboxes = self.delect.detect_face(image)
        area = [(box[2] - box[0]) * (box[3] - box[1]) for box in bboxes]
        area.sort(reverse=True)
        for box in bboxes:
            xmin, ymin, xmax, ymax = box
            if (xmax - xmin) * (ymax - ymin) == area[0]:
                self.image = image[ymin + 3:ymax - 3, xmin + 3:xmax - 3]
                self.disp_label(self.face_lab,self.image)
                self.face_flag = True

    def save(self):
        name = self.name_text.text()
        sex_1 = self.man_radio.isChecked()
        sex_2 = self.women_radio.isChecked()
        sex = "男" if sex_1 else "女"
        born = QtCore.QDate(self.born.date()).toPyDate()
        new_born = QtCore.QDate(QtCore.QDate.currentDate()).toPyDate()
        phone = self.phone_text.text()
        adress = self.adress_text.toPlainText()
        if name == "":
            self.disp_error("姓名不能为空！")
        elif phone == "":
            self.disp_error("手机号码不能为空！")
        elif adress == "":
            self.disp_error("住址不能为空！")
        elif len(phone) < 11:
            self.disp_error("手机号码格式不对！")
        elif new_born == born:
            self.disp_error("请输入出生日期！")
        else:
            image = cv2.resize(self.image, (160, 160))
            image2 = image[np.newaxis, :]
            vectors = self.facenet.run(image2)
            result = self.milvus.select_info(vector=vectors.tolist(), table_name="facetable")
            print("结果:",result)
            if result != -1:
                self.disp_error("错误！不能重复存储。")
            else:
                id = self.milvus.insert_data(vectors.tolist(), "facetable")
                status = self.db.insert_data(id=str(id),
                                             name=name,
                                             sex=sex,
                                             born=str(born),
                                             phone=phone,
                                             adress=adress,
                                             path=self.config.get('ui_event','save_path')+str(id)+'.jpg')

                if status:
                    cv2.imwrite(self.config.get('ui_event','save_path')+str(id)+'.jpg',image)
                    message_box = QtWidgets.QMessageBox
                    message_box.information(self.Form, "OK", "数据存储成功！", message_box.Yes)
                    self.Form.close()
                else:
                    self.milvus.delete_fromid("facetable", id)
                    self.disp_error("数据存储失败！")

    def disp_error(self,mes):
        message_box = QtWidgets.QMessageBox
        message_box.critical(self.Form,"Error",mes,message_box.Yes)


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
    def disp_label(self, label, image):
        image = self._letterbox_image(image.copy(), (label.width(), label.height()))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(label.width(), label.height())  # 设置图片大小
        label.setPixmap(jpg_out)  # 设置图片显示


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FromImageSave()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())