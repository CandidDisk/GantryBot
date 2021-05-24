from piGantry.imageProcess import cameraFunc as camera
import cv2
import time

# Set width & height to high value to set resolution as max 
cam = camera.cameraObj(10000, 10000)

def main():
    img = 0
    img2 = 0
    def grabImg():
        while True:
            try:
                img = cam.grabFrame()
                cv2.imwrite("tests/lRTestImg1.png", img)
                time.sleep(1)
                img2 = cam.grabFrame()
                cv2.imwrite("tests/lRTestImg2.png", img2)
                break
            except Exception as e:
                print("Exception while capture frame: {}".format(e))
        print("camera done")

    grabImg()

    while not camera.compareImg(img, img2, 0.005):
        grabImg()
