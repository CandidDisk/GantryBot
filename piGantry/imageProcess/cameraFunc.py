import cv2
import numpy as np

class cameraObj(object):
    def __init__(self, width, height):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def grabFrame(self, imgName):
        ret, frame = self.cam.read()
        if not ret:
            return "Failed to grab frame"
        self.cam.release()
        return cv2.imwrite(imgName, frame)
        
def preProcImg(img):
    imageGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(imageGray, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    image = cv2.dilate(image, el, iterations=1)
    return image

def retContour(img, minArea, maxArea, exemptArea):

    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    dotCenters = []

    for contour in contours:
        if minArea < cv2.contourArea(contour) < maxArea:
            area = cv2.contourArea(contour)
            
            # Easy way to filter out contours that are too large
            # & or contain multiple contours
            if area > exemptArea:
                continue

            contourMoment = cv2.moments(contour)

            try:
                intensity = img[int(contourMoment['m10'] / contourMoment['m00'])][int(contourMoment['m01'] / contourMoment['m00'])]
                center = (int(contourMoment['m10'] / contourMoment['m00']), int(contourMoment['m01'] / contourMoment['m00']))
                dotCenters.append(center)
            except:
                continue
    
    return dotCenters

def pixelWiseScan(img):
    xRow, yCol = img.shape