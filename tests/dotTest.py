from piGantry.imageProcess import cameraFunc as camera
from piGantry.piSerial import mathFunc as mathFunc
import cv2
import time
import json



# Set width & height to high value to set resolution as max 
cam = camera.cameraObj(10000, 10000)

def main():
    while True:
        try:
            img = cam.grabFrame()
            cv2.imwrite("tests/testImg.png", img)
            break
        except Exception as e:
            print(e)
    print("camera done")

    t3 = time.perf_counter()
    exposureVal = 4
    frameVal = 4

    img2 = cv2.imread("imgData/comparisonExternalPSU/22.56v_{0}/opencv_frame_{1}.png".format(exposureVal, frameVal))
    img3 = cv2.imread("imgData/comparisonExternalPSU/22.81v_{0}/opencv_frame_{1}.png".format(exposureVal, frameVal))
    img4 = cv2.imread("imgData/comparisonExternalPSU/23.17v_{0}/opencv_frame_{1}.png".format(5, frameVal))
    img5 = cv2.imread("imgData/comparisonExternalPSU/23.56v_{0}/opencv_frame_{1}.png".format(5, frameVal))

    #print("compareImg far 1 & 2 {0}\n".format(camera.compareImg(img2,img3, 0.005)))

    
    t1 = time.perf_counter()
    procImg = camera.preProcImg(img2)
    procImg2 = camera.preProcImg(img3)
    procImg3 = camera.preProcImg(img4)
    procImg4 = camera.preProcImg(img5)
    t2 = time.perf_counter()

    print(t2)

    def pixelScan(img):
        print("\npixel start\n")
        t1 = time.perf_counter()
        pixelWise=camera.pixelWiseScan(img, 1, 50)
        t2 = time.perf_counter()
        print("pixel end in {0} \n pixel: {1} \n dots: {2}\n".format((t2-t1),pixelWise,len(pixelWise)))

    def contourScan(img, origImg, imgName, minArea, maxArea, exemptArea):
        print("\ncontour1 start\n")
        t1 = time.perf_counter()
        contours=camera.retContour(img, origImg, minArea, maxArea, exemptArea, "{}Contour.png".format(imgName))
        t2 = time.perf_counter()
        print("contour end in {0} \n contour: {1} \n dots: {2}\n".format((t2-t1),contours[0],len(contours[0])))
        mathFunc.bestFitPoly(contours[1][1], contours[1][0], 4, origImg)
        return contours[0]


    contourList = [contourScan(procImg, img2, "22.56v_5", 5, 50, 100), 
                   contourScan(procImg2, img3, "22.81v_5", 1, 50, 100),
                   contourScan(procImg3, img4, "23.17v_5", 5, 50, 100), 
                   contourScan(procImg4, img5, "23.56v_5", 1, 50, 100)]

    for i in enumerate(contourList):
        with open("dataContour{0}.json".format(i[0]), "w") as write_file:
            json.dump(i[1], write_file, indent=4)


    #with open("dataContour1.json", "w") as write_file:
    #    json.dump(contours1, write_file, indent=4)
    #with open("dataContour2.json", "w") as write_file:
    #    json.dump(contours2, write_file, indent=4)
    #with open("dataContour3.json", "w") as write_file:
    #    json.dump(contours1, write_file, indent=4)
    #with open("dataContour4.json", "w") as write_file:
    #    json.dump(contours2, write_file, indent=4)
    #with open("dataPixel.json", "w") as write_file:
    #    json.dump(pixelWise, write_file, indent=4)

    #print("Passes subtraction: {}".format(passed))
    
main()