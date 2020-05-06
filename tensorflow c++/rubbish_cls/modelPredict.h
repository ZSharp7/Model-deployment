#ifndef MODELPREDICT_H
#define MODELPREDICT_H
 
#include <iostream>
#include <vector>
#include <ctime>
#include <memory>

#include <tensorflow/core/public/session.h>
#include <tensorflow/core/platform/env.h>
#include <opencv2/opencv.hpp>
// #include "tensorflow/core/framework/tensor.h"
// #include "tensorflow/cc/ops/image_ops.h"
// #include "tensorflow/core/platform/types.h"
// #include "tensorflow/core/platform/logging.h"
// #include "tensorflow/core/graph/default_device.h"
// #include "tensorflow/cc/ops/standard_ops.h"
// #include "tensorflow/core/graph/graph_def_builder.h"
// #include "tensorflow/core/framework/graph.pb.h"

using namespace std;
using namespace tensorflow;
using namespace cv;

struct Rubbish{
    int xmin,ymin,xmax,ymax;
    int cls;
    float score;
    int x,y;
};//物体坐标、分类、分数、中心点（图像上的中心点）

class ModelPredict{

private:
	string model_path; // 模型地址
	Session* session; // session
	string input_tensor_name 	= "input_data:0"; // 模型输入节点
	vector<string> output_nodes;  // 模型输出节点  

public:
	ModelPredict(const string& path){
		model_path = path; 
		readPbFromFile(); //载入模型
	}

	void readPbFromFile(); //载入pb模型
	void getBox(Mat image, vector<Rubbish>* result); // 运行网络进行预测
	Tensor readTensor(Mat src); //从Mat(opencv)中读取tensor
    void postProcess(Rubbish* temp, Mat bbox_image);
    static bool sortFun(vector<Point> &p1,vector<Point> &p2);
};
#endif