from milvus import Milvus, MetricType
import configparser

class VisitMilvus:
    def __init__(self):
        self.milvus = Milvus()
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        try:
            self.milvus.connect(host=self.config.get('compare_face','host'), port=self.config.get('compare_face','port'))
            self.status = True
        except:
            self.status = False
        # self.num_vec = 128
        self.vec_dim = int(self.config.get('compare_face','vec_dim'))
        self.table_name = self.config.get('compare_face','table_name')

    def create(self,table_name):
        param = {'collection_name': table_name, 'dimension': self.vec_dim, 'index_file_size': 1024, 'metric_type': MetricType.L2}
        self.milvus.create_collection(param)

    def table_len(self,table_name):
        status,info = self.milvus.collection_info(table_name)
        return info.count



    def insert_data(self,vector,table_name,id=None):
        if id == None:
            length = self.table_len(table_name)
        else:
            length = id
        status,ids = self.milvus.insert(table_name,vector,ids=[length])
        return ids[0]

    def delete_table(self,table_name):
        self.milvus.drop_collection(table_name)

    def delete_fromid(self,table_name,id):
        self.milvus.delete_by_id(table_name,[id])
    def select_info(self,table_name,vector):
        search_param = {'nprobe': 16}
        try:
            status,result = self.milvus.search(collection_name=table_name, query_records=vector, top_k=1, params=search_param)
            id = result[0][0].id
            distance = result[0][0].distance
            print("L2距离：",distance)
            if distance<=float(self.config.get('compare_face','distance')):
                return id
            else:
                return -1
        except:
            return -1

if __name__ == '__main__':
    from code.face_detect import FaceDR
    from code.face_net import FaceNet
    import numpy as np
    import cv2
    # image = cv2.imread('../data/load_model.jpg')
    # image = cv2.imread('../data/db/img/2.jpg')

    # delect = FaceDR()
    # box = delect.detect_face(image)
    # xmin, ymin, xmax, ymax = box[0]
    # image = image[ymin + 3:ymax - 3, xmin + 3:xmax - 3]
    #
    # cv2.imshow("imamge",image)
    # cv2.waitKey(0)
    # image = cv2.resize(image, (160, 160))
    # image = image[np.newaxis, :]

    # vectors = FaceNet().run(image)


    db = VisitMilvus()
    table_name = "facetable"
    # db.create(table_name)
    # db.disp_table_info("facetable")
    # print(db.insert_data(vectors.tolist(),'facetable'))
    # db.show_table("facetable")
    # length = db.table_len(table_name)
    # db.delete_table(table_name)

    # result = db.select_info(table_name,vectors.tolist())

    print(db.table_len(table_name))
    # db.delete_fromid(table_name,4)