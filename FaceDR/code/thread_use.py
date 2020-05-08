from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class CameraThread(QThread):
    tarigger = pyqtSignal()
    def __init__(self):
        super(CameraThread,self).__init__()
        self.working = True
        self.num = 0
    def __del__(self):
        self.wait()
    def run(self):

        self.tarigger.emit()
    def stop(self):
        self.working = False
