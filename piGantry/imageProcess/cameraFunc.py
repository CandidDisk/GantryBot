import cv2
import numpy as np

#Initializes camera as new instance of opencv videocapture class when called on
class cameraObj(object):
    def __init__(self, width, height):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def grabFrame(self):
        ret, frame = self.cam.read()
        if not ret:
            return "Failed to grab frame"
        self.cam.release()
        return frame
        
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

    refDot = []
    dataFinal = []
    dotArr = []

    count = 0
    prevLength = 0

    for i in range(xRow):
        pointRow = {"xRow": int(i),
                    "yCol": []}
        for j in range(yCol):
            pixel = img[i,j]
            if (pixel == 0):
                num = count - 1
                
                if (int(j) not in pointRow["yCol"]):
                    pointRow["yCol"].append(int(j))
                if (pointRow not in refDot):
                    refDot.append(pointRow)
                    count += 1
                    try:
                        if (i - refDot[num]["xRow"] <= 1):
                            if (pointRow not in dotArr):
                                dotArr.append(pointRow)
                        else:
                            dotArr = []
                    except:
                        continue
        if (count > 0):
            try:
                if (len(dotArr) == prevLength):
                    if (len(dotArr) > 2):
                        colLast = 0
                        colFirst = 0
                        rowFirst = dotArr[0]["xRow"]
                        try:
                            rowLast = dotArr[len(dotArr)-1]["xRow"]
                        except:
                            continue
                        for i in dotArr:
                            lastVal = i["yCol"][len(i["yCol"])-1]
                            firstVal = i["yCol"][0]
                            if (colLast == 0 and colFirst == 0):
                                colLast = lastVal
                                colFirst = firstVal
                            else:
                                if (firstVal < colFirst):
                                    colFirst = firstVal
                                if (lastVal > colLast):
                                    colLast = lastVal
                        centreObj = {"x": int((colFirst + colLast)/2),
                                    "y": int((rowFirst + rowLast)/2)}
                        obj = {
                            "dot": dotArr,
                            "rowFirst": rowFirst,
                            "rowLast": rowLast,
                            "colFirst": colFirst,
                            "colLast": colLast,
                            "centre": centreObj
                        }
                        if (obj not in dataFinal):
                            dataFinal.append(obj)
                prevLength = len(dotArr)
            except:
                continue
    return dataFinal