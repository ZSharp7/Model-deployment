# 测试Tensorflow C++ Bazel（CPU）
## 版本
* tensorflow = 1.13.1
* bazel = 0.19.2
## 安装bazel
* chmod -x 文件名
* ./文件名
* bazel version 验证安装
## 编译tensorflow
* ./configure进行配置
* bazel build --config=opt //tensorflow:libtensorflow_cc.so

## 使用了yolo3的三分类目标检测，测通，可以直接移植。
