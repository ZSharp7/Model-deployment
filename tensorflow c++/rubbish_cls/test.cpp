#include <iostream>
#include <vector>
#include <io.h>
#include <string>

#include "modelPredict.h"
#include "modelPredict.cpp"

using namespace std;
using namespace cv;
// 测试程序
int main(){
    string model_path = "/mnt/i/ubuntu/user/zsharp/project/demo/data/tiny_freeze.pb"; // 模型地址
    string image_path = "/mnt/i/ubuntu/user/zsharp/project/demo/data/image.jpg"; // 图片地址
    string image_dir = "/mnt/i/ubuntu/user/zsharp/project/demo/data/test_img/*.jpg";
	Mat image;
    vector<Rubbish> result; // 定义输出
    vector<Scalar> colors;
    colors.push_back(Scalar(255,0,0));
    colors.push_back(Scalar(0,255,0));
    colors.push_back(Scalar(0,0,255));
    vector<string> classes;
    classes.push_back("塑料瓶");
    classes.push_back("纸盒");
    classes.push_back("易拉罐");


	image = imread(image_path);
    ModelPredict model(model_path);

    model.getBox(image,&result); // 得到输出
    cout << "[LOG] predict_result: " << endl;
    for(int i=0; i<result.size(); i++){
        rectangle(image,Point(result[i].xmin,result[i].ymin),Point(result[i].xmax,result[i].ymax),colors[result[i].cls],2,8,0);
        circle(image,Point(result[i].x,result[i].y), 10, Scalar(0,255,0), -1);
        cout << classes[result[i].cls] << " " <<  result[i].score<< " " << result[i].xmin << ", " << result[i].ymin << ", "<<result[i].xmax << ", "<< result[i].ymax << endl;
        cout << "center: " << result[i].x << " " << result[i].y << endl; 
    }
    imwrite("/mnt/i/ubuntu/user/zsharp/project/demo/data/image2.jpg",image);
}