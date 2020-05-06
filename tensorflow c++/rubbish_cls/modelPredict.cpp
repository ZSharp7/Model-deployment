
void ModelPredict::readPbFromFile(){
	output_nodes.push_back("output/concat:0"); //输出节点
	output_nodes.push_back("output/concat_1:0");
	output_nodes.push_back("output/concat_2:0");

	Status status = NewSession(SessionOptions(), &session);//创建session
	GraphDef graphdef;
	Status status_load = ReadBinaryProto(Env::Default(), model_path, &graphdef);//读取模型
	if (!status_load.ok()){
		cout << "[Error] Loading model failed." << model_path << endl;
		cout << status_load.ToString() << endl;
	}

	Status status_create = session->Create(graphdef); //模型导入session
	if (!status_create.ok()){
		cout << "[Error] Create graph in session failed." << status_create.ToString() << endl;
		cout << status_load.ToString() << endl;
   	}
   	cout << "[LOG] Model is loaded in " << model_path <<endl;
}


void ModelPredict::getBox(Mat image, vector<Rubbish>* result){
	
	clock_t start_time,end_time;	
	start_time = clock();
	vector<Tensor> inputs; // 输入tensor
    vector<Tensor> outputs; // 输出tensor

	inputs.push_back(readTensor(image)); // 数据载入
	cout << "\n[LOG]data_time: " <<(double)(clock()-start_time)/CLOCKS_PER_SEC << endl;
	Status status_run = session->Run( // 运行网络
		{{input_tensor_name,inputs[0]}},
		output_nodes,
		{} ,&outputs
	);
	end_time = clock();
	result->clear(); // 清空输出
	double use_time = (double)(end_time-start_time)/CLOCKS_PER_SEC;
	cout<<"[LOG]toal_time: "<<use_time<<endl;

	if (!status_run.ok()) {
	    cout << "ERROR: RUN failed..."  << endl;
	    cout << status_run.ToString() << "\n";
    }
	auto bbox = outputs[0].tensor<float, 2>(); // 坐标
	auto scores = outputs[1].tensor<float, 1>(); // 分数
	auto classes = outputs[2].tensor<int, 1>(); // 分类
	int pred_num = outputs[0].dim_size(0); // 图片中物体数量
	
	for(int i=0; i<pred_num; i++){
		Rubbish temp;
		Rect im_select;
		temp.xmin = bbox(i, 1);
		temp.ymin = bbox(i, 0);
		temp.xmax = bbox(i, 3);
		temp.ymax = bbox(i, 2);
		temp.x = 0;
		temp.y = 0;
		im_select = Rect(temp.xmin,temp.ymin,temp.xmax-temp.xmin,temp.ymax-temp.ymin);
		postProcess(&temp, image(im_select));
		
		// imwrite("/mnt/i/ubuntu/user/zsharp/project/demo/data/bbox.jpg",image(im_select));
		temp.cls = classes(i);
		temp.score = scores(i);
		result->push_back(temp); // 返回输出
	}
	
	inputs.clear();	
	outputs.clear();

}

void ModelPredict::postProcess(Rubbish* temp, Mat bbox_image){
	Mat image;
	GaussianBlur(bbox_image, image, Size(5, 5), 1.5); // 高斯模糊
	cvtColor(image,image,CV_BGR2GRAY); // 转灰度图
	threshold(image,image,0,255,THRESH_BINARY|THRESH_TRIANGLE); // 阈值分割

	Mat ele = getStructuringElement(MORPH_RECT, Size(5,5));
	morphologyEx(image,image,MORPH_OPEN,ele,Size(-1,-1),3);
	vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
	findContours(image, contours, hierarchy,CV_RETR_TREE , CV_CHAIN_APPROX_SIMPLE);
	sort(contours.begin(),contours.end(),sortFun);
	
	auto M = moments(contours[0]);
	temp->x = M.m10 / M.m00 + temp->xmin;
	temp->y = M.m01 / M.m00 + temp->ymin;

	// imwrite("/mnt/i/ubuntu/user/zsharp/project/demo/data/bbox.jpg",image);
}
bool ModelPredict::sortFun(vector<Point> &p1,vector<Point> &p2){
	double p1_area = contourArea(p1);
	double p2_area = contourArea(p2);
	return p1_area > p2_area;

}

Tensor ModelPredict::readTensor(Mat src){
	Tensor input_tensor(DT_FLOAT,TensorShape({1,src.rows,src.cols,3}));
	auto tmap = input_tensor.tensor<float,4>();
	
	for(int i=0;i<src.rows;i++){//Mat复制到Tensor
		for(int j=0;j<src.cols;j++){
			tmap(0,i,j,0)=src.at<Vec3b>(i, j)[0];
			tmap(0,i,j,1)=src.at<Vec3b>(i, j)[1];
			tmap(0,i,j,2)=src.at<Vec3b>(i, j)[2];
		}
	}
	return input_tensor;
}
