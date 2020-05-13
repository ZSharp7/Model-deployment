import tensorflow as tf
import cv2
import numpy as np
import configparser

class FaceNet:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.model_path = self.config.get('face_net','pb_model')
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        self.return_elements = ["input:0","phase_train:0","embeddings:0"]
        self.return_tensors = self._read_pb_return_tensors(self.graph, self.model_path, self.return_elements)


    def _read_pb_return_tensors(self,graph, pb_file, return_elements):

        with tf.gfile.FastGFile(pb_file, 'rb') as f:
            frozen_graph_def = tf.GraphDef()
            frozen_graph_def.ParseFromString(f.read())

        with graph.as_default():
            return_elements = tf.import_graph_def(frozen_graph_def,
                                                  return_elements=return_elements)
        return return_elements

    def run (self,image):
        emb = self.sess.run(
            self.return_tensors[2],feed_dict={
                self.return_tensors[0]:image,
                self.return_tensors[1]:False
            }
        )
        return emb

if __name__ == '__main__':
    image = cv2.imread('../data/image2.jpg')
    image = cv2.resize(image,(160,160))
    # image = np.asarray(image, np.float32)
    image = image[np.newaxis,:]
    emb = FaceNet().run(image)
    print(len(emb[0]))

