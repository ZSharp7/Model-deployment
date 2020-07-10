//
//  pictureRecognition.cpp
//  MNN
//
//  Created by MNN on 2018/05/14.
//  Copyright © 2018, Alibaba Group Holding Limited
//
  
#include <stdio.h>
#include "MNN/ImageProcess.hpp"
#include "MNN/Interpreter.hpp"

#define MNN_OPEN_TIME_TRACE

#include <algorithm>
#include <fstream>
#include <functional>
#include <memory>
#include <sstream>
#include <vector>
#include "MNN/AutoTime.hpp"
#include <sys/time.h>

#define STB_IMAGE_IMPLEMENTATION

// #include "stb_image.h"
// #include "stb_image_write.h"
#include <iostream>
#include <opencv2/opencv.hpp>
#include <fstream>
#include <algorithm>

using namespace MNN::CV;
using std::cin;
using std::endl;
using std::cout;
using namespace std;
using namespace cv;
using namespace MNN;

struct Object {
    cv::Rect_<float> rect;
    int label;
    float prob;
};


class Read_MNN
{

    private:
        std::vector<std::string> class_names = {"suliaoping","zhihe","yilaguan"};
        const float NMS_THRES = 0.45f;
        const float CONF_THRES = 0.4f;
        const int num_category=int(class_names.size());
        std::shared_ptr<MNN::Interpreter> net;
        std::vector<int> shape;
        int pad_W,pad_H;
        int input_H,input_W;
        MNN::Session *session       = nullptr;
        MNN::Tensor *input   = nullptr;
        double ratio;
    public:
        
        Read_MNN(const std::string &model_path, int threads=4, int precision=2, int forward = MNN_FORWARD_CPU){
            cout << "模型读取。。" << endl;
            //  模型读取
            net = std::shared_ptr<Interpreter>(Interpreter::createFromFile(model_path.c_str()));
            ScheduleConfig config;
            config.numThread    = threads;
            config.type         = static_cast<MNNForwardType>(forward);

            session = net->createSession(config);
            input = net->getSessionInput(session, NULL);
            shape = input->shape();        
            input_H=shape[1];
            input_W=shape[2];
            net->resizeTensor(input, shape);
            net->resizeSession(session);
        }

        ~Read_MNN(){
            net -> releaseModel();
            net -> releaseSession(session);
        };

        Mat processImg(Mat raw_image){

            // auto inputPatch = "./data/123.jpg";
            // raw_image = cv::imread(inputPatch);
            cv::cvtColor(raw_image, raw_image, cv::COLOR_BGR2RGB);
            
            int ori_height = raw_image.rows;
            int ori_width = raw_image.cols;
            
            ratio = std::min(1.0 * input_H / ori_height, 1.0 * input_W / ori_width);
            int resize_height = int(ori_height * ratio);
            int resize_width = int(ori_width * ratio);
            //odd number->pad size error
            if (resize_height%2!=0) resize_height-=1;
            if (resize_width%2!=0) resize_width-=1;

            pad_W = int((input_W - resize_width) / 2);
            pad_H = int((input_H - resize_height) / 2);
            cv::Scalar pad(128, 128, 128);
            cv::Mat resized_image;
            cv::resize(raw_image, resized_image, cv::Size(resize_width, resize_height), 0, 0, cv::INTER_LINEAR);
            cv::copyMakeBorder(resized_image, resized_image, pad_H, pad_H, pad_W, pad_W, cv::BORDER_CONSTANT, pad);
            resized_image.convertTo(resized_image, CV_32FC3);
            resized_image = resized_image / 255.0f;

            cout << "模型预处理。。。" << endl;
            return resized_image;
            
        }

        int run(Mat image,std::vector<Object>* objects){

            
            image = processImg(image);
            // wrapping input tensor, convert nhwc to nchw
            std::vector<int> dim{1, input_H, input_W, 3};
            auto nhwc_Tensor = MNN::Tensor::create<float>(dim, NULL, MNN::Tensor::TENSORFLOW);
            auto nhwc_data = nhwc_Tensor->host<float>();
            auto nhwc_size = nhwc_Tensor->size();
            ::memcpy(nhwc_data, image.data, nhwc_size);
            input->copyFromHostTensor(nhwc_Tensor);

            cout << "运行模型。。"<< endl;
            net->runSession(session);
            cout << "运行结束。。"<< endl;
            auto output = net->getSessionOutput(session, NULL);
            auto dimType = output->getDimensionType();
            if (output->getType().code != halide_type_float) {
                dimType = Tensor::TENSORFLOW;
            }

            std::shared_ptr<Tensor> outputUser(new Tensor(output, dimType));
            output->copyToHostTensor(outputUser.get());
            auto type = outputUser->getType();

            auto size = outputUser->elementSize();
            std::vector<float> tempValues(size);
            if (type.code == halide_type_float) {
                auto values = outputUser->host<float>();
                for (int i = 0; i < size; ++i) {
                    tempValues[i] = values[i];
                }
            }

            auto OUTPUT_NUM = outputUser->shape()[0];
            std::vector<std::vector<Object> > class_candidates(20);
            std::vector<int> tempcls;

            for (int i = 0; i < OUTPUT_NUM; ++i) {
                auto prob = tempValues[i * (5+num_category) + 4];
                auto maxcls = std::max_element(tempValues.begin() + i * (5+num_category) + 5, tempValues.begin() + i * (5+num_category) + (5+num_category));
                auto clsidx = maxcls - (tempValues.begin() + i * (5+num_category) + 5);
                auto score = prob * (*maxcls);
                if (score < CONF_THRES) continue;
                auto xmin = (tempValues[i * (5+num_category) + 0] - pad_W) / ratio;
                auto xmax = (tempValues[i * (5+num_category) + 2] - pad_W) / ratio;
                auto ymin = (tempValues[i * (5+num_category) + 1] - pad_H) / ratio;
                auto ymax = (tempValues[i * (5+num_category) + 3] - pad_H) / ratio;

                Object obj;
                obj.rect = cv::Rect_<float>(xmin, ymin, xmax - xmin + 1, ymax - ymin + 1);
                obj.label = clsidx;
                obj.prob = score;
                class_candidates[clsidx].push_back(obj);
            }
            
            for (int i = 0; i < (int) class_candidates.size(); i++) {
                std::vector<Object> &candidates = class_candidates[i];

                qsort_descent_inplace(candidates);

                std::vector<int> picked;
                nms_sorted_bboxes(candidates, picked, NMS_THRES);

                for (int j = 0; j < (int) picked.size(); j++) {
                    int z = picked[j];
                    objects->push_back(candidates[z]);
                }
            }
            return 0;
            // auto imgshow = draw_objects(raw_image, objects);
            // cv::imwrite("./image.jpg",imgshow);
            // cv::imshow("w", imgshow);
            // cv::waitKey(-1);
            // return 0;
        }

        static void qsort_descent_inplace(std::vector<Object> &objects, int left, int right) {
            int i = left;
            int j = right;
            float p = objects[(left + right) / 2].prob;

            while (i <= j) {
                while (objects[i].prob > p)
                    i++;

                while (objects[j].prob < p)
                    j--;

                if (i <= j) {
                    // swap
                    std::swap(objects[i], objects[j]);

                    i++;
                    j--;
                }
            }

            // #pragma omp parallel sections
            // {
            //     #pragma omp section{
            //         if (left < j) qsort_descent_inplace(objects, left, j);
            //     }
            //     #pragma omp section
            //     {
            //          if (i < right) qsort_descent_inplace(objects, i, right);
            //     }
            // }
        }

        void qsort_descent_inplace(std::vector<Object> &objects) {
            if (objects.empty())
                return;

            qsort_descent_inplace(objects, 0, objects.size() - 1);
        }

        inline float intersection_area(const Object &a, const Object &b) {
            cv::Rect_<float> inter = a.rect & b.rect;
            return inter.area();
        }

        void nms_sorted_bboxes(const std::vector<Object> &objects, std::vector<int> &picked, float NMS_THRES) {
            picked.clear();

            const int n = objects.size();

            std::vector<float> areas(n);
            for (int i = 0; i < n; i++) {
                areas[i] = objects[i].rect.area();
            }

            for (int i = 0; i < n; i++) {
                const Object &a = objects[i];

                int keep = 1;
                for (int j = 0; j < (int) picked.size(); j++) {
                    const Object &b = objects[picked[j]];

                    // intersection over union
                    float inter_area = intersection_area(a, b);
                    float union_area = areas[i] + areas[picked[j]] - inter_area;
                    //float IoU = inter_area / union_area
                    if (inter_area / union_area > NMS_THRES)
                        keep = 0;
                }

                if (keep)
                    picked.push_back(i);
            }
        }

        cv::Mat draw_objects(const cv::Mat &rgb, const std::vector<Object> &objects) {

            cv::Mat image = rgb.clone();
            cv::cvtColor(image, image, cv::COLOR_RGB2BGR);
            for (size_t i = 0; i < objects.size(); i++) {
                const Object &obj = objects[i];

                fprintf(stderr, "%d = %.5f at %.2f %.2f %.2f x %.2f\n", obj.label, obj.prob,
                        obj.rect.x, obj.rect.y, obj.rect.width, obj.rect.height);

                cv::rectangle(image, obj.rect, cv::Scalar(255, 0, 0));

                char text[256];
                sprintf(text, "%s %.1f%%", class_names[obj.label].c_str(), obj.prob * 100);

                int baseLine = 0;
                cv::Size label_size = cv::getTextSize(text, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);

                int x = obj.rect.x;
                int y = obj.rect.y - label_size.height - baseLine;
                if (y < 0)
                    y = 0;
                if (x + label_size.width > image.cols)
                    x = image.cols - label_size.width;

                cv::rectangle(image, cv::Rect(cv::Point(x, y),
                                              cv::Size(label_size.width, label_size.height + baseLine)),
                              cv::Scalar(255, 255, 255), -1);

                cv::putText(image, text, cv::Point(x, y + label_size.height),
                            cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0));
            }
            return image;
        }


};





int main() {
    char const *filename = "../data/123.jpg";
    Read_MNN model("../data/quant.mnn");
    std::vector<Object> rubbish;
    Mat image = cv::imread(filename);
    model.run(image,&rubbish);
    image = model.draw_objects(image,rubbish);
    cv::imwrite("./image.jpg",image);
    return 0;
}

// g++ yolo.cpp -o test `pkg-config --libs --cflags opencv,mnn` -ldl
