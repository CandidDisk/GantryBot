import cv2
import time
import numpy as np
from piGantry.imageProcess import cameraFunc as camera
import matplotlib.pyplot as plt


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1632*0.8)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1224*0.8)
#cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
#cam.set(cv2.CAP_PROP_EXPOSURE, -6)

width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('your_video.avi', fourcc, 20.0, size)
#out = cv2.VideoWriter('output.avi', -1, 20.0, (height,width))

frame = False

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, '', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)

GRID_SIZE = 20


while True:
    comparedVal = [["Compared Img", "# of pixel", "# above thresh", "Max val"]]
    k = cv2.waitKey(1)
    ret, frame = cam.read()
    #print(height, width)
    height = frame.shape[1]
    width = frame.shape[0]
    channel = frame.shape[2]
    center = (int(height/2), int(width/2))
    #for x in range(0, width -1, GRID_SIZE):
    #    cv2.line(frame, (x, 0), (x, height), (255, 0, 0), 1, 1)
    cv2.line(frame, (0, int(width/2)), (height, int(width/2)), (0, 255, 0), thickness=3, lineType=8)
    #cv2.line(frame, (int(width), 0), (int(width/2), height), (0, 255, 0), thickness=3, lineType=8)
    #print(center)
    cv2.circle(frame,center, 10, (0,0,0), -1)
    if ret:
        cv2.imshow('Frame',frame)
        cv2.setMouseCallback('Frame', click_event)
        out.write(frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cam.release()
out.release()
cv2.destroyAllWindows()

# center : H 1632, W 1224
# H 1491, W 1212