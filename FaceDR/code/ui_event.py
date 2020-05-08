import os
import configparser
import time
from PyQt5 import QtWidgets,QtGui,QtCore,Qt
import sys
from PyQt5.QtCore import QTimer
import cv2
from PIL import Image
import numpy as np
import threading
from compare_face import VisitMilvus
from database import DB
from save_face import Ui_Form
from show_data import ShowData
from image_tosave import FromImageSave
from ui_design import Ui_MainWindow
from thread_use import CameraThread
from face_detect import FaceDR
from face_net import  FaceNet

class Event(Ui_MainWindow):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.save_path = self.config.get('ui_event', 'save_path')

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.setWindowIcon(QtGui.QIcon(self.config.get('ui_event', 'icon')))
        self.camera_btn.setEnabled(False)
        self.printf("界面构造成功。")
        # milvus
        self.milvus = VisitMilvus()
        if self.milvus.status == False:
            self.printf("Milvus connect is failed.")
        else:
            self.printf("Milvus is connected.")
        self.tablename = 'facetable'
        # camera
        self.cap = cv2.VideoCapture(0)
        # model
        self.detect = FaceDR()
        self.detect_flag = False
        self.facenet = FaceNet()
        self.face_times = 0
        self.face_flag = True
        # mysql
        self.db = DB()

        # 相机拍照
        self.camera_thread = CameraThread()
        self.camera_thread.tarigger.connect(self._load_image)
        self.camera_time = QTimer()
        self.camera_time.timeout.connect(lambda : self.camera_thread.start())
        # 模型初始化
        self.model_thread = threading.Thread(target=self._init_model)
        self.model_thread.start()
        # 按钮函数连接信号槽
        self.add_data_btn.clicked.connect(self.add_data)
        self.camera_btn.clicked.connect(self._start_camera)
        # 菜单栏栏信号槽
        self.show_m.triggered.connect(self.show_data)
        self.save_m.triggered.connect(self.save_from_image)

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


    def add_data(self):

        '''
        截取人脸图片，调用子窗口，存储数据到mysql和milvus中
        :return:
        '''
        self.printf("增加数据。。")
        self.camera_time.stop()
        self.camera_btn.setEnabled(True)
        self.MainWindow2 = QtWidgets.QMainWindow()
        id = self.milvus.table_len(self.tablename)
        # print(self.save_path+str(id) + '.jpg')
        try:
            # cv2.imwrite(os.path.join(self.save_path,str(id)+'.jpg'),self.face_img)
            # print('文件写入成功。')
            self.Ui_Form = Ui_Form(id,self.facenet,
                                   self.db,
                                   self.milvus,
                                   self.face_img,
                                   os.path.join(self.save_path,str(id)+'.jpg'))
            self.Ui_Form.setupUi(self.MainWindow2)
            self.MainWindow2.show()
        except:
            print(' is error')

    def save_from_image(self):
        self.camera_time.stop()
        self.camera_btn.setEnabled(True)

        self.MainWindow_fromImage = QtWidgets.QMainWindow()
        self.ui = FromImageSave(self.detect,self.facenet)
        self.ui.setupUi(self.MainWindow_fromImage)
        self.MainWindow_fromImage.show()


    def show_data(self):
        self.camera_time.stop()
        self.camera_btn.setEnabled(True)

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
        self.db = DB()
        self.printf("Start Camera and Using model.")
        self.cap = cv2.VideoCapture(0)
        self.camera_time.start(100)
        # self.facenet_time.start(2000)
        self.printf("FaceNet 向量生成速度2s/次. ")
        self.camera_btn.setEnabled(False)

    def get_emb(self):
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
        if data == None:
            output = ''
            image = cv2.imread(self.config.get('ui_event','background_image'))
            image = cv2.resize(image,(121,151))
        else:
            output = "ID：%d\n姓名：%s\n性别：%s\n出生日期：%s\n手机号：%s\n地址：%s"%(
                data['id'],data['name'],data['sex'],data['born'],data['phone'],data['adress'])
            image = cv2.imread(data['image_path'])

        self.info_text.setPlainText(output)  # 在指定的区域显示提示信息
        self.disp_label(self.face_lab,image)

    def _load_image(self):

        self.face_times += 1
        ret, frame = self.cap.read()
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
                        self.get_emb()
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),1)
            if len(bboxes) <= 0:
                self.face_img = None
        self.disp_label(self.camera_lab,frame)

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Event().run()
