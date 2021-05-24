from piGantry.imageProcess import cameraFunc as camera
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

    img2 = cv2.imread("4_21v/opencv_frame_0.png")
    img3 = cv2.imread("4_21v/opencv_frame_6.png")

    print("compareImg far 1 & 2 {0}\n".format(camera.compareImg(img2,img3, 0.005)))

    
    t1 = time.perf_counter()
    procImg = camera.preProcImg(img2)
    procImg2 = camera.preProcImg(img3)
    t2 = time.perf_counter()

    print(t2)

    
    print("\npixel start\n")
    t1 = time.perf_counter()
    pixelWise=camera.pixelWiseScan(procImg, 1, 50)
    t2 = time.perf_counter()
    print("pixel end in {0} \n pixel: {1} \n dots: {2}\n".format((t2-t1),pixelWise,len(pixelWise)))

    
    print("\ncontour1 start\n")
    t1 = time.perf_counter()
    contours1=camera.retContour(procImg2, 1, 50, 100, "image2test.png")
    t2 = time.perf_counter()
    print("contour1 end in {0} \n contour: {1} \n dots: {2}\n".format((t2-t1),contours1,len(contours1)))

    print("\ncontour2 start\n")
    t1 = time.perf_counter()
    contours2=camera.retContour(procImg, 1, 50, 100, "image3test.png")
    t2 = time.perf_counter()
    print("contour2 end in {0} \n contour: {1} \n dots: {2}\n".format((t2-t1),contours2,len(contours2)))

    t1 = time.perf_counter()
    passed = camera.compareContour(contours1, contours2, (1, 1), (-1, -1))
    t2 = time.perf_counter()

    t4 = time.perf_counter()

    print("compare end in {0}\n".format((t2-t1)))


    print("contour & compare end in {0}".format((t4-t3)))

    with open("dataContour1.json", "w") as write_file:
        json.dump(contours1, write_file, indent=4)
    with open("dataContour2.json", "w") as write_file:
        json.dump(contours2, write_file, indent=4)
    with open("dataPixel.json", "w") as write_file:
        json.dump(pixelWise, write_file, indent=4)

    print("Passes subtraction: {}".format(passed))
    
main()