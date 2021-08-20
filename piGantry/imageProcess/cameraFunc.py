import cv2
import numpy as np
import time
import json


from operator import itemgetter

#Initializes camera as new instance of opencv videocapture class when called on
class cameraObj(object):
    def __init__(self, width, height, exposure):
        self.cam = cv2.VideoCapture(1)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cam.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def grabFrame(self):
        ret, frame = self.cam.read()
        print(ret)
        print(frame)
        if ret:
            frameReturn = np.array(frame)
            return frameReturn
        
        
def preProcImg(img):
    t1 = time.perf_counter()
    #img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    #y, u, v = cv2.split(img_yuv)
    #l_channel = cv2.cvtColor(img_yuv, cv2.COLOR_RGB2LUV)[:, :, 0]
    imageGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(imageGray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    el = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    image = cv2.dilate(image, el, iterations=1)
    t2 = time.perf_counter()
    print("preProcImg end in {0}\n".format((t2-t1)))
    return image

def retContour(img, origImg, minArea, maxArea, exemptArea, file):
    image2 = np.zeros((2448,3264,3),np.uint8)
    backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    writeFile = origImg

    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    xCoords = []
    yCoords = []

    dotCenters = []
    plotCoords = [xCoords, yCoords]

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
                plotCoords[0].append(contourMoment['m10'] / contourMoment['m00'])
                plotCoords[1].append(contourMoment['m01'] / contourMoment['m00'])
                dotCenters.append(center)
                cv2.circle(writeFile,center, 1, (255,0,0), -1)
            except:
                continue
    cv2.imwrite(file, writeFile)
    # x, y
    return (dotCenters, plotCoords)


def pixelWiseScan(img, minPix, maxPix):
    image3 = np.zeros((2448,3264,3),np.uint8)
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
                    cv2.circle(image3,center, 1, (255,0,0), -1)
                    
                    dataFinal.append(center)
                    
                dotArr = []
                dotArr.append((int(nonZero[0][i]), int(nonZero[1][i])))
            else:
                dotArr.append((int(nonZero[0][i]), int(nonZero[1][i])))
        except:
            continue

    cv2.imwrite("image4test.png", image3)

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

# Subtracts two images & returns new imsub array + max value & # of pixels through threshold
def compareImg(img1, img2, thresh, imgName):
    imgGray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    imgGray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diffArr = cv2.subtract(imgGray1, imgGray2)

    imgMean = np.mean(diffArr)
    nonZero = np.nonzero(diffArr)
    
    print(imgMean)
    

    foo = [["X", "Y", "Subtracted", "Original 1", "Original 2"]]

    numThresh = 0
    maxVal = 0

    for i in range(len(nonZero[0])):
        #if (int(imgGray1[nonZero[0][i-1], nonZero[1][i-1]]) > 30 and 30 < int(imgGray2[nonZero[0][i-1], nonZero[1][i-1]])):
        try:
            foo1 = [int(nonZero[1][i-1]), int(nonZero[0][i-1]), int(diffArr[nonZero[0][i-1], nonZero[1][i-1]]),int(imgGray1[nonZero[0][i-1], nonZero[1][i-1]]),int(imgGray2[nonZero[0][i-1], nonZero[1][i-1]])]
            foo.append(foo1)
            if (int(diffArr[nonZero[0][i-1], nonZero[1][i-1]]) > maxVal):
                maxVal = int(diffArr[nonZero[0][i-1], nonZero[1][i-1]])
            #cv2.circle(img1,(nonZero[1][i-1], nonZero[0][i-1]), 1, (255,0,0), -1)
        except:
            continue

        # If pixel is over threshold
        if (int(diffArr[nonZero[0][i-1], nonZero[1][i-1]]) > 50):
            numThresh += 1

    #cv2.imwrite("{}.png".format(imgName), img1)
    foo2 = [imgName, len(foo), numThresh, maxVal]

    print(len(foo))

    return (foo, foo2)
    #return diffArr


def returnTBDot(retContour, retContourM):
    width = 3264
    dotCenters = retContour[0]
    dotCentersM = retContourM[0]

    dotT = dotCenters[0]
    dotB = dotCenters[len(dotCenters)-1]

    dotTM = dotCentersM[0]
    dotBM = dotCentersM[len(dotCentersM)-1]

    dotUnflipTMX = width - dotTM[0]-1
    dotUnflipBMX = width - dotBM[0]-1

    diffTop = dotT[0] - dotUnflipTMX
    diffBtm = dotB[0] - dotUnflipBMX

    print((diffTop, diffBtm))
    return diffTop, diffBtm
    
