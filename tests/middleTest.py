from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc

from piGantry.imageProcess import cameraFunc as camera
from piGantry.piSerial import mathFunc as mathFunc

import cv2
import time
import json
import numpy as np
21
# Set width & height to high value to set resolution as max 
#cam = camera.cameraObj(10000, 10000, -3)

# Initialize new motor object for state management
motorX = motorFunc.motor(19.98145313)
motorY = motorFunc.motor(19.98626075)

motorGroup = (motorX, motorY)

# Initialize new serialObject instances for each device
#microX = serialComm.serialObject(9600, "COM8")    
#microY = serialComm.serialObject(9600, "COM14")  
#clearCoreX = serialComm.serialObject(1000000, "COM18")
#clearCoreY = serialComm.serialObject(1000000, "COM7")

def testFunc(img):
    imgFlip = cv2.flip(img, 1)
    procImg = camera.preProcImg(img)
    procImgFlip = camera.preProcImg(imgFlip)
    contours=camera.retContour(procImg, img, 1, 50, 100, "{}Contour.png".format("img"))
    contoursFlip=camera.retContour(procImgFlip, imgFlip, 1, 50, 100, "{}Contour.png".format("imgFlip"))

    cv2.imwrite("mirrored.png", imgFlip)
    cv2.imwrite("img.png", procImg)
    cv2.imwrite("imgMirrored.png", procImgFlip)
    
    print(contours[0][0])
    print(contours[0][len(contours[0])-1])

    print(contoursFlip[0][0])
    print(contoursFlip[0][len(contoursFlip[0])-1])

    print(img.shape[1]-contours[0][0][0]-1)

def main():
    img = cv2.imread("imgData/comparisonExternalPSU/23.56v_5/opencv_frame_5.png")
    img2 = cv2.imread("imgData/comparisonExternalPSU/23.56v_5/opencv_frame_5.png")
    procImg = camera.preProcImg(img)
    contours=camera.retContour(procImg, img, 1, 50, 100, "{}Contour.png".format("img"))

    translation_matrix = np.float32([[1, 0, 10], [0, 1, 0]])
    imgTrans1 = cv2.warpAffine(procImg, translation_matrix, (procImg.shape[1], procImg.shape[0]))
    contoursT1=camera.retContour(imgTrans1, img, 1, 50, 100, "{}Contour.png".format("imgT1"))
    translation_matrix = np.float32([[1, 0, 15], [0, 1, 0]])
    imgTrans2 = cv2.warpAffine(procImg, translation_matrix, (procImg.shape[1], procImg.shape[0]))
    contoursT2=camera.retContour(imgTrans2, img, 1, 50, 100, "{}Contour.png".format("imgT2"))
    translation_matrix = np.float32([[1, 0, 20], [0, 1, 0]])
    imgTrans3 = cv2.warpAffine(procImg, translation_matrix, (procImg.shape[1], procImg.shape[0]))
    contoursT3=camera.retContour(imgTrans3, img, 1, 50, 100, "{}Contour.png".format("imgT3"))

    procTransFlip1 = cv2.flip(imgTrans1, 1)
    contoursTF1=camera.retContour(procTransFlip1, img, 1, 50, 100, "{}Contour.png".format("imgTF1"))
    procTransFlip2 = cv2.flip(imgTrans2, 3)
    contoursTF2=camera.retContour(procTransFlip2, img, 1, 50, 100, "{}Contour.png".format("imgTF2"))
    procTransFlip3 = cv2.flip(imgTrans3, 3)
    contoursTF3=camera.retContour(procTransFlip3, img, 1, 50, 100, "{}Contour.png".format("imgTF3"))

    stepsToMove = 50
    diff=camera.returnTBDot(contoursT1, contoursTF3)
    print(f"Move {stepsToMove} steps")
    diff2=camera.returnTBDot(contoursT1, contoursTF2)
    diff3 = np.subtract(diff,diff2)
    print(f"diff3 = {diff3}")
    pixelPerStepT = float(diff3[0]/stepsToMove)
    pixelPerStepB = float(diff3[1]/stepsToMove)
    print(pixelPerStepT, pixelPerStepB)
    camera.returnTBDot(contoursT1, contoursTF1)
    cv2.imwrite("origImg.png", img2)
    cv2.imwrite("imgTrans1.png", imgTrans1)
    cv2.imwrite("imgTrans2.png", imgTrans2)
    cv2.imwrite("imgTrans3.png", imgTrans3)

    #camera.returnTBDot(contours, img)
    
main()

