
#项目名称
project(test)
#设置c++编译器
set(CMAKE_CXX_STANDARD 11)
#设置TENSORFLOW_DIR变量，变量内容为安装的tensorflow文件夹路径
set(TENSORFLOW_DIR /mnt/i/ubuntu/user/zsharp/project/demo/include)

set(TENSORFLOW_DIRA /mnt/i/ubuntu/user/zsharp/project/demo/lib)
#项目中的include路径
include_directories(${TENSORFLOW_DIR} //tensorFlow头文件
                    ${TENSORFLOW_DIR}/tensorflow/contrib/makefile/gen/proto //tensorflow pb文件生成的pb.h头文件
                    ${TENSORFLOW_DIR}/tensorflow/contrib/makefile/gen/protobuf-host/include //protobuf头文件
                    ${TENSORFLOW_DIR}/tensorflow/contrib/makefile/downloads/eigen //eigen头文件
                    ${TENSORFLOW_DIR}/tensorflow/contrib/makefile/downloads/nsync/public //nsync头文件
					${TENSORFLOW_DIR}/tensorflow/contrib/makefile/downloads/absl
					)
 
#项目中lib路径

link_directories(${TENSORFLOW_DIRA}/tensorflow/contrib/makefile/gen/lib //tensorflow静态库
                 ${TENSORFLOW_DIRA}/tensorflow/contrib/makefile/gen/protobuf-host/lib //protobuf静态库
                 ${TENSORFLOW_DIRA}/bazel-bin/tensorflow //tensorflow动态库
                 ${TENSORFLOW_DIRA}/tensorflow/contrib/makefile/downloads/nsync/builds /default. linux.c++11 //nsync静态库
                 ${TENSORFLOW_DIRA})
 
add_executable(test test.cpp)
#连接libtensorflow_cc.so和libtensorflow_framework库。
target_link_libraries(test tensorflow_cc tensorflow_framework opencv_dnn opencv_highgui opencv_ml opencv_objdetect opencv_shape opencv_stitching opencv_superres opencv_videostab opencv_calib3d opencv_videoio opencv_imgcodecs opencv_features2d opencv_video opencv_photo opencv_imgproc opencv_flann opencv_core)
