from piGantry.imageProcess import cameraFunc as camera
import cv2
import time

cam = camera.cameraObj(10000, 10000, -4, 0)
print("woo")
cam2 = camera.cameraObj(10000, 10000, -4, 1)
print("waa")

def main():
    cv2.imwrite("camTest1.png", cam.grabFrame())
    cv2.imwrite("camTest2.png", cam2.grabFrame())
    print("Camera done")
    cam.cam.release()

main()