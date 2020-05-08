# Opencv + Yolo3-Tiny + FaceNet + Milvus + MySQL + PyQt5
# 视频人脸检测识别软件
## 环境
* opencv-python: 3.4.2.16
* Milvus: 0.8.0
* MySQL: 5.6.0
* PyQt5: 5.12.1
* Tensorflow: 1.13.1
* Python: 3.7/3.5
* Anaconda3等其他Python环境

## 简述
1. 使用opencv调用摄像头
2. 检测每一帧人脸
3. 生成特征向量
4. milvus进行向量检索和保存
5. mysql存储milvus库中对应向量id的个人信息（姓名，性别等）
6. pyqt5设计界面

## 功能
1. 存储人脸和对应信息
2. 检测人脸和显示对应信息
3. 显示数据库，提供删除操作
4. 存储人脸方式：视频截取关键帧、本地图片

## 模型
1. Yolo3-Tiny预测：130ms
2. FaceNet+MySQL查询+Milvus检索： 120ms
3. 实时人脸检测约为7-8帧，人脸识别使用另一个单线程。

时间：2020.5.8