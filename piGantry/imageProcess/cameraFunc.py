import cv2
import numpy as np
import time

from operator import itemgetter

#Initializes camera as new instance of opencv videocapture class when called on
class cameraObj(object):
    def __init__(self, width, height):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cam.set(cv2.CAP_PROP_EXPOSURE, 0.05)

    def grabFrame(self):
        ret, frame = self.cam.read()
        if not ret:
            return "Failed to grab frame"
        self.cam.release()
        return frame
        
def preProcImg(img):
    t1 = time.perf_counter()
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    #y, u, v = cv2.split(img_yuv)
    l_channel = cv2.cvtColor(img_yuv, cv2.COLOR_RGB2LUV)[:, :, 0]
    #imageGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(l_channel, 20, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    el = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    image = cv2.dilate(image, el, iterations=1)
    t2 = time.perf_counter()
    print("preProcImg end in {0}\n".format((t2-t1)))
    return image

def retContour(img, minArea, maxArea, exemptArea, file):
    #image2 = np.zeros((2448,3264,3),np.uint8)

    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    dotCenters = []

    for contour in contours:
        # Check dot area 
        if minArea < cv2.contourArea(contour) < maxArea:
            area = cv2.contourArea(contour)
            
            # Easy way to filter out contours that are too large
            # & or contain multiple contours
            if area > exemptArea:
                continue

            contourMoment = cv2.moments(contour)

            try:
                #intensity = img[int(contourMoment['m10'] / contourMoment['m00'])][int(contourMoment['m01'] / contourMoment['m00'])]
                center = (int(contourMoment['m10'] / contourMoment['m00']), int(contourMoment['m01'] / contourMoment['m00']))
                dotCenters.append(center)
                #cv2.circle(image2,center, 1, (255,0,0), -1)
            except:
                continue
    #cv2.imwrite(file, image2)
    # x, y
    return dotCenters


def pixelWiseScan(img, minPix, maxPix):
    #image3 = np.zeros((2448,3264,3),np.uint8)
    threshPixel = []
    dotArr = []
    dataFinal = []

    # Flattens threshold array into dimension for x & for y
    nonZero = np.nonzero(img)

    def getCenter(dot):
        xCenter = int((min(dot, key=itemgetter(1))[1] + max(dot, key=itemgetter(1))[1])/2)
        yCenter = int((min(dot, key=itemgetter(0))[0] + max(dot, key=itemgetter(0))[0])/2)
        return (xCenter, yCenter)

    for i in range(len(nonZero[0])):
        # Formatting key of both dimensions into x, y tuple
        threshPixel.append((int(nonZero[0][i]), int(nonZero[1][i])))
        try:
            # Subtract current x,y tuple w/ previous 
            priorDiff = tuple(map(lambda x, y: x - y, threshPixel[i], threshPixel[i-1]))
            if (priorDiff[0] > 1):
                # Check dot area 
                if (minPix < len(dotArr) < maxPix):
                    center = getCenter(dotArr)
                    #cv2.circle(image3,center, 1, (255,0,0), -1)
                    dataFinal.append(center)
                    
                dotArr = []
                dotArr.append((int(nonZero[0][i]), int(nonZero[1][i])))
            else:
                dotArr.append((int(nonZero[0][i]), int(nonZero[1][i])))
        except:
            continue

    #cv2.imwrite("image4test.png", image3)

    # inverts array 
    return dataFinal[::-1]

# compareContour(contourArray1, contourArray2, (maxValX, maxValY), (minValX, minValY))
def compareContour(arr1, arr2, maxTuple, minTuple):
    try:
        subtracted = np.subtract(arr1, arr2)
        maxVal = (max(subtracted, key=itemgetter(0))[0], max(subtracted, key=itemgetter(1))[1])
        minVal = (min(subtracted, key=itemgetter(0))[0], min(subtracted, key=itemgetter(1))[1])
        if (maxVal <= maxTuple and minTuple <= minVal):
            return True
        else:
            return False
    except:
        return False

def compareImg(img1, img2, thresh):
    imgGray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    imgGray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diffArr = cv2.subtract(imgGray1, imgGray2)

    imgMean = np.mean(diffArr)
    nonZero = np.nonzero(diffArr)
    imgMean2 = np.mean(nonZero)


    if (imgMean < thresh):
        return True
    else:
        return False
    #return diffArr
