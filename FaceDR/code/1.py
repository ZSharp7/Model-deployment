import cv2
num = 0
cap = cv2.VideoCapture(num + cv2.CAP_DSHOW)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    cv2.imshow("cap",frame)
    cv2.waitKey(100)