from piGantry.imageProcess import cameraFunc as camera
import cv2

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

    img2 = cv2.imread("tests/gray.png")
    
    procImg = camera.preProcImg(img2)
    print(camera.retContour(procImg, 2, 50, 100))
    print("\n")
    print(camera.pixelWiseScan(procImg))

main()