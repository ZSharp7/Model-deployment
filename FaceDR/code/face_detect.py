# _*_ coding:utf-8 _*_

import numpy as np
import cv2
# import dlib
import time
import tensorflow as tf
import os
import configparser

SCALE_FACTOR = 1
FEATHER_AMOUNT = 11

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 60))
MOUTN_POINTS2 = [48,61,62,63,64,54]
MOUTN_POINTS3 = [48,67,66,65,54]
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 36))
NOSE_POINTS2 = [27,31]
NOSE_POINTS3 = [27,35,30]
JAW_POINTS = list(range(0, 17))

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]
COLOUR_CORRECT_BLUR_FRAC = 0.8

class FaceDR:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.pb_model = self.config.get('face_detect','pb_model')
        # self.detector = dlib.get_frontal_face_detector()
        # self.predictor = dlib.shape_predictor('../data/model/shape_predictor_68_face_landmarks.dat')
        self.return_elements = ["input_data:0", "output/concat:0", "output/concat_1:0", "output/concat_2:0"]
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        self.return_tensors = self._read_pb_return_tensors(self.graph, self.pb_model, self.return_elements)

    def detect_face(self,image_data):
        shape = image_data.shape[:2]
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        # print(self.return_tensors)
        bbox = self.sess.run(
            self.return_tensors[1],
            feed_dict={self.return_tensors[0]: image_data})
        bboxes = []
        for i in bbox:
            ymin,xmin,ymax,xmax = [int(j) for j in i]
            xmax = max(0, np.floor(xmax + 0.5).astype('int32'))
            xmin = max(0, np.floor(xmin + 0.5).astype('int32'))
            ymax = min(shape[1], np.floor(ymax + 0.5).astype('int32'))
            ymin = min(shape[0], np.floor(ymin + 0.5).astype('int32'))
            bboxes.append([xmin,ymin,xmax,ymax])
        # # 人脸数rects
        # rects = self.detector(image, 0)
        return bboxes
    def _read_pb_return_tensors(self,graph, pb_file, return_elements):

        with tf.gfile.FastGFile(pb_file, 'rb') as f:
            frozen_graph_def = tf.GraphDef()
            frozen_graph_def.ParseFromString(f.read())

        with graph.as_default():
            return_elements = tf.import_graph_def(frozen_graph_def,
                                                  return_elements=return_elements)
        return return_elements
    def detect_point(self,image,bboxes):
        result_point = []
        for i in range(len(bboxes)):
            box = dlib.rectangle(int(bboxes[i][1]),int(bboxes[i][0]),int(bboxes[i][3]),int(bboxes[i][2]))
            landmarks = np.matrix([[p.x, p.y] for p in self.predictor(image, box).parts()])
            points = []
            for idx,point in enumerate(landmarks):
                # 坐标
                pos = (point[0,0], point[0,1])
                points.append(pos)
            result_point.append(points)
        return result_point

    def run(self,image,is_point=True):
        start_time = time.time()
        bboxes = self.detect_face(image)
        if is_point == False:
            return bboxes
        points = self.detect_point(image,bboxes)
        end_time = time.time()
        print("[LOG] Tims: %.4f"%(end_time-start_time))
        for id,point in enumerate(points):
            box = bboxes[id]
            image = cv2.rectangle(image,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
            for pos in point:
                cv2.circle(image,pos, 2, (0,255,0), -1)
            cv2.polylines(image,[np.array(point)[LEFT_BROW_POINTS]],False,(0,255,0))
            cv2.polylines(image,[np.array(point)[RIGHT_BROW_POINTS]],False,(0,255,0))
            cv2.polylines(image,[np.array(point)[LEFT_EYE_POINTS]],True,(0,255,0))
            cv2.polylines(image,[np.array(point)[RIGHT_EYE_POINTS]],True,(0,255,0))
            cv2.polylines(image,[np.array(point)[MOUTH_POINTS]],True,(0,255,0))
            cv2.polylines(image,[np.array(point)[MOUTN_POINTS2]],False,(0,255,0))
            cv2.polylines(image,[np.array(point)[MOUTN_POINTS3]],False,(0,255,0))


            cv2.polylines(image,[np.array(point)[JAW_POINTS]],False,(0,255,0))
            cv2.polylines(image,[np.array(point)[NOSE_POINTS]],False,(0,255,0))
            cv2.polylines(image,[np.array(point)[NOSE_POINTS2]],True,(0,255,0))
            cv2.polylines(image,[np.array(point)[NOSE_POINTS3]],True,(0,255,0))


        return image

    def camera(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame,1)
            # img = self.run(frame)
            this_time = time.time()
            # img = self.swap_face(frame)
            img = self.run(frame)
            print("time: ",time.time()-this_time)
            cv2.imshow("cap",np.array(img,dtype=np.uint8))
            cv2.waitKey(10)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def swap_face(self,image):
        def transformation_from_points(points1, points2):
            """
            Return an affine transformation [s * R | T] such that:
                sum ||s*R*p1,i + T - p2,i||^2
            is minimized.
            """
            # Solve the procrustes problem by subtracting centroids, scaling by the
            # standard deviation, and then using the SVD to calculate the rotation. See
            # the following for more details:
            #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

            points1 = points1.astype(np.float64)
            points2 = points2.astype(np.float64)

            c1 = np.mean(points1, axis=0)
            c2 = np.mean(points2, axis=0)
            points1 -= c1
            points2 -= c2

            s1 = np.std(points1)
            s2 = np.std(points2)
            points1 /= s1
            points2 /= s2

            U, S, Vt = np.linalg.svd(points1.T * points2)

            # The R we seek is in fact the transpose of the one given by U * Vt. This
            # is because the above formulation assumes the matrix goes on the right
            # (with row vectors) where as our solution requires the matrix to be on the
            # left (with column vectors).
            R = (U * Vt).T

            return np.vstack([np.hstack(((s2 / s1) * R,
                                               c2.T - (s2 / s1) * R * c1.T)),
                                 np.matrix([0., 0., 1.])])

        def draw_convex_hull(im, points, color):
            points = cv2.convexHull(points)
            cv2.fillConvexPoly(im, points, color=color)

        def get_face_mask(im, landmarks):
            im = np.zeros(im.shape[:2], dtype=np.float64)

            for group in OVERLAY_POINTS:
                draw_convex_hull(im,
                                 landmarks[group],
                                 color=1)

            im = np.array([im, im, im]).transpose((1, 2, 0))

            im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
            im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

            return im

        def warp_im(im, M, dshape):
            output_im = np.zeros(dshape, dtype=im.dtype)
            cv2.warpAffine(im,
                           M[:2],
                           (dshape[1], dshape[0]),
                           dst=output_im,
                           borderMode=cv2.BORDER_TRANSPARENT,
                           flags=cv2.WARP_INVERSE_MAP)
            return output_im

        def correct_colours(im1, im2, landmarks1):
            blur_amount = COLOUR_CORRECT_BLUR_FRAC * np.linalg.norm(
                np.mean(landmarks1[LEFT_EYE_POINTS], axis=0) -
                np.mean(landmarks1[RIGHT_EYE_POINTS], axis=0))
            blur_amount = int(blur_amount)
            if blur_amount % 2 == 0:
                blur_amount += 1
            im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
            im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

            # Avoid divide-by-zero errors.
            im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

            return (im2.astype(np.float64) * im1_blur.astype(np.float64) /
                    im2_blur.astype(np.float64))

        def read_im_and_landmarks(fname,is_file=True):
            if is_file:
                im = cv2.imread(fname, cv2.IMREAD_COLOR)
            else:
                im = cv2.cvtColor(fname,cv2.IMREAD_COLOR)
            im = cv2.resize(im, (im.shape[1] * SCALE_FACTOR,
                                 im.shape[0] * SCALE_FACTOR))
            bboxes = self.detect_face(im)
            if len(bboxes) > 1:
                print("to many faces")
                os._exit(0)
            bbox = bboxes[0]
            box = dlib.rectangle(int(bbox[1]), int(bbox[0]), int(bbox[3]), int(bbox[2]))
            landmarks = np.matrix([[p.x, p.y] for p in self.predictor(im, box).parts()])
            return im, landmarks


        im1,landmarks1 = read_im_and_landmarks(image,is_file=False)
        im2,landmarks2 = read_im_and_landmarks("./data/image3.jpg")

        M = transformation_from_points(landmarks1,landmarks2)

        mask = get_face_mask(im2,landmarks2)

        warped_mask = warp_im(mask,M,im1.shape)
        combined_mask = np.max([get_face_mask(im1, landmarks1), warped_mask],
                          axis=0)
        warped_im2 = warp_im(im2, M, im1.shape)
        warped_corrected_im2 = correct_colours(im1, warped_im2, landmarks1)

        # output_im = im1 * (1.0 - combined_mask) +  combined_mask
        output_im = im1 * (1.0 - combined_mask) + warped_corrected_im2 * combined_mask

        return output_im


if __name__ == '__main__':
    FaceDR().camera()


# # cv2读取图像
# img = cv2.imread("./data/load_model.jpg")
#
# # 取灰度
# img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#
#
# for i in range(len(rects)):
#     print(rects[i])
#     landmarks = np.matrix([[p.x, p.y] for p in predictor(img, rects[i]).parts()])
#     for idx, point in enumerate(landmarks):
#         # 68点的坐标
#         pos = (point[0, 0], point[0, 1])
#         print(idx + 1, pos)
#
#         # 利用cv2.circle给每个特征点画一个圈，共68个
#         cv2.circle(img, pos, 2, color=(0, 255, 0))
#         # 利用cv2.putText输出1-68
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(img, str(idx + 1), pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
#
# cv2.namedWindow("img", 2)
# cv2.imshow("img", img)
# cv2.waitKey(0)