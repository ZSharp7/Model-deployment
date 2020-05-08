import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
from code.face_detect import FaceDR


class Ui:
    def __init__(self,tk):
        self.window = tk
        self.setup_ui()



    def setup_ui(self):
        # 主窗口
        self.window.title("测试程序")
        self.window.resizable(False, False)
        sw = self.window.winfo_screenwidth()  # 获取屏幕宽
        sh = self.window.winfo_screenheight()  # 获取屏幕高
        wx = 1024
        wh = 600
        self.window.geometry("%dx%d+%d+%d" % (wx, wh, (sw - wx) / 2, (sh - wh) / 2))
        # 画布
        self.canvas = tk.Canvas(self.window,bg='#c4c2c2',height=300,width=1024)
        self.canvas.place_configure(x=0,y=0)
        # 摄像头线程
        th_camera = threading.Thread(target=self.camera)
        th_camera.setDaemon(True)
        # camera 按钮
        self.btn = tk.Button(self.window, text="开启摄像头", command=lambda: th_camera.start(), width=10, height=2)
        self.btn.place_configure(x=5, y=310)
        self.btn['state'] = tk.DISABLED
        # 日志窗口
        self.log_txt = tk.Text(self.window,width=50,height=10)
        self.log_txt.place_configure(x=100,y=310)
        # self.log_txt.selection_handle(index=)
        # self.log_txt['state'] = tk.DISABLED

        # 人脸检测模型初始化线程
        threading.Thread(target=self.model_init).start()

    def camera(self):
        self.printf("打开摄像头.")
        cap = cv2.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            frame = cv2.flip(frame,1)
            bboxes = self.detect.detect_face(frame)
            area = [(box[2] - box[0]) * (box[3] - box[1]) for box in bboxes]
            area.sort(reverse=True)
            for box in bboxes:
                xmin,ymin,xmax,ymax = box
                if (xmax - xmin) * (ymax - ymin) == area[0] and area[0] >= 50000:
                    self.printf(area[0])
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = self.letterbox_image(Image.fromarray(frame),(400,300))
            image_file = ImageTk.PhotoImage(frame)
            self.canvas.create_image(0, 0, anchor='nw', image = image_file)
            # time.sleep(0.03)
            # canvas.after(1,camera)

    def letterbox_image(self,image, size):
        '''resize image with unchanged aspect ratio using padding'''
        iw, ih = image.size
        w, h = size
        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = image.resize((nw, nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128, 128, 128))
        new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
        return new_image

    def printf(self,mes):
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_txt.insert("[%s] %s\n"%(date,mes))

    def model_init(self):
        self.printf("开始载入人脸检测模型.")
        self.detect = FaceDR()
        load_image = "../data/load_model.jpg"
        image = cv2.imread(load_image)
        self.detect.detect_face(image)
        self.printf("人脸检测模型载入成功.")

        self.btn['state'] = tk.NORMAL

# threading.Thread(target=camera).start()
if __name__ == '__main__':
    window = tk.Tk()
    main = Ui(window)
    window.mainloop()
