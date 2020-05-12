#项目名称
project(yolo)
#设置c++编译器
set(CMAKE_CXX_STANDARD 11)
#设置TENSORFLOW_DIR变量，变量内容为安装的tensorflow文件夹路径
set(TENSORFLOW_DIR /mnt/i/MNN-yolo3)

#项目中的include路径
include_directories(${TENSORFLOW_DIR}/include)
#项目中lib路径
link_directories(${TENSORFLOW_DIR}/lib)
 
add_executable(test yolo.cpp)
#连接lib库。
target_link_libraries(test opencv_dnn opencv_highgui opencv_ml opencv_objdetect opencv_shape opencv_stitching opencv_superres opencv_videostab opencv_calib3d opencv_videoio opencv_imgcodecs opencv_features2d opencv_video opencv_photo opencv_imgproc opencv_flann opencv_core MNN)
