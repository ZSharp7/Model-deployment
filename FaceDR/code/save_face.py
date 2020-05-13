# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_face.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import os
import cv2
import configparser
from PIL import Image
import numpy as np
from code.database import DB

class Ui_Form(QtWidgets.QWidget):
    def __init__(self,facenet,milvus,image,save_path):
        super(Ui_Form,self).__init__()
        self.db = DB()
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.save_path = self.config.get('ui_event', 'save_path')
        self.path = save_path
        self.image = image
        self.facenet = facenet
        self.milvus = milvus


    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        Form.setWindowModality(QtCore.Qt.ApplicationModal)

        Form.resize(426, 346)
        # 禁止拉伸窗口大小
        Form.setFixedSize(Form.width(), Form.height())

        self.image_lab = QtWidgets.QLabel(Form)
        self.image_lab.setGeometry(QtCore.QRect(40, 60, 121, 141))
        self.image_lab.setStyleSheet("background-color: rgb(173, 173, 173);")
        self.image_lab.setText("")
        self.image_lab.setObjectName("image_lab")
        self.name_lab = QtWidgets.QLabel(Form)
        self.name_lab.setGeometry(QtCore.QRect(180, 62, 54, 21))
        self.name_lab.setObjectName("name_lab")
        self.sex_lab = QtWidgets.QLabel(Form)
        self.sex_lab.setGeometry(QtCore.QRect(180, 92, 41, 31))
        self.sex_lab.setObjectName("sex_lab")
        self.born_lab = QtWidgets.QLabel(Form)
        self.born_lab.setGeometry(QtCore.QRect(180, 132, 61, 21))
        self.born_lab.setObjectName("born_lab")
        self.phone_lab = QtWidgets.QLabel(Form)
        self.phone_lab.setGeometry(QtCore.QRect(180, 174, 54, 20))
        self.phone_lab.setObjectName("phone_lab")
        self.adress_lab = QtWidgets.QLabel(Form)
        self.adress_lab.setGeometry(QtCore.QRect(180, 200, 51, 31))
        self.adress_lab.setObjectName("adress_lab")
        self.id_lab = QtWidgets.QLabel(Form)
        self.id_lab.setGeometry(QtCore.QRect(180, 22, 31, 21))
        self.id_lab.setObjectName("id_lab")
        self.id_text = QtWidgets.QLineEdit(Form)
        self.id_text.setGeometry(QtCore.QRect(250, 22, 81, 21))
        self.id_text.setObjectName("id_text")
        self.name_text = QtWidgets.QLineEdit(Form)
        self.name_text.setGeometry(QtCore.QRect(250, 62, 81, 21))
        self.name_text.setMaxLength(3)
        self.name_text.setObjectName("name_text")
        self.man_radio = QtWidgets.QRadioButton(Form)
        self.man_radio.setGeometry(QtCore.QRect(250, 92, 51, 31))
        self.man_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.man_radio.setChecked(True)
        self.man_radio.setObjectName("radioButton")
        self.women_radio = QtWidgets.QRadioButton(Form)
        self.women_radio.setGeometry(QtCore.QRect(300, 92, 51, 31))
        self.women_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.women_radio.setChecked(False)
        self.women_radio.setObjectName("radioButton_2")
        self.born = QtWidgets.QDateEdit(Form)
        self.born.setGeometry(QtCore.QRect(250, 132, 81, 21))
        self.born.setObjectName("dateEdit")
        self.phone_text = QtWidgets.QLineEdit(Form)
        self.phone_text.setGeometry(QtCore.QRect(250, 172, 113, 21))
        self.phone_text.setMaxLength(11)
        self.phone_text.setObjectName("phone_text")
        self.adress_text = QtWidgets.QPlainTextEdit(Form)
        self.adress_text.setGeometry(QtCore.QRect(250, 210, 161, 71))
        self.adress_text.setObjectName("adress_text")
        self.ok_btn = QtWidgets.QPushButton(Form)
        self.ok_btn.setGeometry(QtCore.QRect(120, 310, 75, 23))
        self.ok_btn.setObjectName("pushButton")
        self.cancel_btn = QtWidgets.QPushButton(Form)
        self.cancel_btn.setGeometry(QtCore.QRect(220, 310, 75, 23))
        self.cancel_btn.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.born.setDate(QtCore.QDate.currentDate())
        self.ok_btn.clicked.connect(self.send)
        self.cancel_btn.clicked.connect(Form.close)
        self.disp_label(self.image_lab,self.image)
        self.Form = Form

    def disp_label(self, label, image):
        image = self._letterbox_image(image.copy(), (label.width(), label.height()))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(label.width(), label.height())  # 设置图片大小
        label.setPixmap(jpg_out)  # 设置图片显示

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "数据录入"))
        Form.setWindowIcon(QtGui.QIcon(self.config.get('show_data', 'icon')))
        self.name_lab.setText(_translate("Form", "姓名："))
        self.sex_lab.setText(_translate("Form", "性别："))
        self.born_lab.setText(_translate("Form", "出生日期："))
        self.phone_lab.setText(_translate("Form", "手机号："))
        self.adress_lab.setText(_translate("Form", "地址："))
        self.id_lab.setText(_translate("Form", "Id:"))
        self.man_radio.setText(_translate("Form", "男"))
        self.women_radio.setText(_translate("Form", "女"))
        self.ok_btn.setText(_translate("Form", "确定"))
        self.cancel_btn.setText(_translate("Form", "取消"))

    def send(self):
        id = self.id_text.text()
        name = self.name_text.text()
        sex_1 = self.man_radio.isChecked()
        sex_2 = self.women_radio.isChecked()
        sex = "男" if sex_1 else "女"
        born =QtCore.QDate(self.born.date()).toPyDate()
        new_born = QtCore.QDate(QtCore.QDate.currentDate()).toPyDate()
        phone = self.phone_text.text()
        adress = self.adress_text.toPlainText()
        if self.db.select_id(id):
            self.disp_error("ID不能重复！")
        elif id == "":
            self.disp_error("ID不能为空！")
        elif name=="":
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
            image = cv2.resize(self.image,(160,160))
            image2 = image[np.newaxis,:]
            vectors = self.facenet.run(image2)
            result = self.milvus.select_info(vector=vectors.tolist(),table_name="facetable")
            if result != -1:
                self.disp_error("不可重复存储。")
            else:
                self.milvus.insert_data(vectors.tolist(),"facetable",id=int(id))
                status = self.db.insert_data(id=str(id),
                                    name=name,
                                    sex=sex,
                                    born=str(born),
                                    phone=phone,
                                    adress=adress,
                                    path = self.path+id+'.jpg')
                cv2.imwrite(self.path+id+'.jpg', image)
                if status:
                    message_box = QtWidgets.QMessageBox
                    message_box.information(self,"OK","数据存储成功！",message_box.Yes)
                    self.Form.close()
                else:
                    self.milvus.delete_fromid("facetable",id)
                    self.disp_error("数据存储失败！")

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

    def disp_error(self,mes):
        message_box = QtWidgets.QMessageBox
        message_box.critical(self,"Error",mes,message_box.Yes)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())