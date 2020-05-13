import os
import configparser
import win32api
import time
from PyQt5 import QtWidgets,QtGui,QtCore,Qt
import sys
from PyQt5.QtCore import QTimer
import cv2
from PIL import Image
import numpy as np
import threading
from code.compare_face import VisitMilvus
from code.database import DB
from code.save_face import Ui_Form
from code.show_data import ShowData
from code.image_tosave import FromImageSave
from code.ui_design import Ui_MainWindow
from code.thread_use import CameraThread
from code.face_detect import FaceDR
from code.face_net import  FaceNet

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.thread_status = True
    def closeEvent(self,event):
        result = QtWidgets.QMessageBox.question(self,
                                            "退出",
                                            "是否退出?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        event.ignore()
        if result == QtWidgets.QMessageBox.Yes:
            self.thread_status = False
            event.accept()


class Event(Ui_MainWindow):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.save_path = self.config.get('ui_event', 'save_path')
        self.camera_number = 0
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = window()
        self.setupUi(self.MainWindow)
        self.MainWindow.setWindowIcon(QtGui.QIcon(self.config.get('ui_event', 'icon')))
        self.camera_btn.setEnabled(False)
        self.printf("界面构造成功。")
        self.emb_flag = True
        # milvus
        self.milvus = VisitMilvus()
        if self.milvus.status == False:
            self.printf("Milvus connect is failed.")
        else:
            self.printf("Milvus is connected.")
        self.tablename = 'facetable'
        # camera
        self.cap = cv2.VideoCapture(self.camera_number + cv2.CAP_DSHOW)
        # model
        self.detect = FaceDR()
        self.detect_flag = False
        self.facenet = FaceNet()
        self.face_times = 0
        self.face_flag = True
        # mysql
        self.db = DB()
        self.emb_db = DB()
        self.camera_lock = threading.Lock()
        # 相机拍照
        self.camera_thread = threading.Thread(target=self._load_image)

        # self.camera_thread.tarigger.connect(self._load_image)
        # self.camera_time = QTimer()
        # self.camera_time.timeout.connect(lambda : threading.Thread(target=self._load_image).start())

        # 模型初始化
        self.model_thread = threading.Thread(target=self._init_model)
        self.model_thread.start()
        # 按钮函数连接信号槽
        self.add_data_btn.clicked.connect(self.add_data)
        self.camera_btn.clicked.connect(self._start_camera)
        # 菜单栏栏信号槽
        self.show_m.triggered.connect(self.show_data)
        self.save_m.triggered.connect(self.save_from_image)
        self.setting_m.triggered.connect(self.setting)
        self.about_m.triggered.connect(self.about)

    def _init_model(self):
        '''
        初始化模型，利用线程在软件打开时进行初始化
        :return:
        '''
        self.printf("Face Detect model is loading.")
        load_image = self.config.get('ui_event','load_image')
        image = cv2.imread(load_image)
        self.detect.detect_face(image)
        self.printf("Face Detect model is loaded.")
        self.printf("FaceNet model is loading.")
        image = cv2.resize(image,(160,160))
        image = image[np.newaxis, :]
        self.facenet.run(image)
        self.printf("FaceNet model is loaded.")
        self.camera_btn.setEnabled(True)
        self.detect_flag = True

    def about(self):
        # self.camera_time.stop()
        # self.camera_btn.setEnabled(True)
        print('display_info ')
        message_box = QtWidgets.QMessageBox
        message_box.information(self.Form, "About", "毕设项目--人脸检测识别器(2020.5)", message_box.Yes)

    def setting(self):
        '''
        菜单栏，设置命令，使用win记事本打开配置文件
        :return:
        '''
        self.printf("打开配置文件.")
        # self.camera_time.stop()
        # self.camera_btn.setEnabled(True)
        win32api.ShellExecute(0, 'open', 'notepad.exe', './config.ini', '', 1)

    def add_data(self):

        '''
        截取人脸图片，调用子窗口，存储数据到mysql和milvus中
        :return:
        '''
        self.printf("增加数据。。")
        # self.camera_time.stop()
        # self.camera_btn.setEnabled(True)
        self.MainWindow2 = QtWidgets.QMainWindow()
        # id = self.milvus.table_len(self.tablename)

        try:
            self.Ui_Form = Ui_Form(self.facenet,
                                   self.milvus,
                                   self.face_img,
                                   self.save_path)
            self.Ui_Form.setupUi(self.MainWindow2)
            self.MainWindow2.show()
        except:
            print(' is error')

    def save_from_image(self):
        '''
        菜单栏存储数据命令，从本地图片中导入数据至数据库中
        :return:
        '''
        # self.camera_time.stop()
        # self.camera_btn.setEnabled(True)

        self.MainWindow_fromImage = QtWidgets.QMainWindow()
        self.ui = FromImageSave(self.detect,self.facenet)
        self.ui.setupUi(self.MainWindow_fromImage)
        self.MainWindow_fromImage.show()


    def show_data(self):
        '''
        菜单栏，显示数据命令，从mysql中读取数据并显示
        :return:
        '''
        # self.camera_time.stop()
        # self.camera_btn.setEnabled(True)

        self.MainWindow_show = QtWidgets.QMainWindow()
        self.ui = ShowData()
        self.ui.setupUi(self.MainWindow_show)
        self.MainWindow_show.show()

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

    def _start_camera(self):
        '''
        开始相机线程
        :return:
        '''
        self.db = DB()
        self.printf("Start Camera and Using model.")

        self.camera_thread.start()
        self.printf("FaceNet 向量生成速度2s/次. ")
        self.camera_btn.setEnabled(False)

    def get_emb(self):
        '''
        生成人脸特征向量，并人脸检索和检索信息显示
        :return:
        '''

        image = self.face_img.copy()
        face_img = self._letterbox_image(image,(160, 160))
        face_img = face_img[np.newaxis,:]
        vectors = self.facenet.run(face_img)
        result = self.milvus.select_info(self.tablename,vectors.tolist())
        print("结果：",result)
        if result != -1:
            data = self.db.select(str(result))
            self.disp_info(data)
        else:
            self.disp_info(None)


    def disp_info(self,data):
        '''
        显示人脸检索到的信息
        :param data:
        :return:
        '''
        if data == None:
            output = ''
            image = cv2.imread(self.config.get('ui_event','background_image'))
            image = cv2.resize(image,(130,130))
        else:
            output = "ID：%d\n姓名：%s\n性别：%s\n出生日期：%s\n手机号：%s\n地址：%s"%(
                data['id'],data['name'],data['sex'],data['born'],data['phone'],data['adress'])

            image = cv2.imread(data['image_path'])
        self.info_text.setText(output)  # 在指定的区域显示提示信息
        self.disp_label(self.face_lab,image)

    def _load_image(self):
        '''
        相机线程
        :return:
        '''
        while True:
            if self.Form.thread_status == False:
                break
            self.face_times += 1
            ret, frame = self.cap.read()
            if ret == False:
                for i in range(3):
                    self.printf('第%d次，相机重连。。'%i)
                    self.cap = cv2.VideoCapture(0)
                    ret,frame = self.cap.read()
                    if ret:
                        break
            frame = cv2.flip(frame,1)
            if self.detect_flag:
                bboxes = self.detect.run(frame,False)
                area = [(box[2]-box[0])*(box[3]-box[1])  for box in bboxes]
                area.sort(reverse=True)
                if len(bboxes) < 1:
                    self.disp_info(None)
                for box in bboxes:
                    xmin,ymin,xmax,ymax = box
                    if (xmax-xmin)*(ymax-ymin) == area[0]:
                        if self.face_times % 10 == 0:
                            self.face_img = frame[ymin+3:ymax-3, xmin+3:xmax-3]
                            try:
                                threading.Thread(target=self.get_emb).start()
                            except:
                                print('识别异常。')
                        cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),1)
                if len(bboxes) <= 0:
                    self.face_img = None
            self.disp_label(self.camera_lab,frame)
    def run(self):
        '''
        开始运行
        :return:
        '''
        self.MainWindow.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Event().run()
