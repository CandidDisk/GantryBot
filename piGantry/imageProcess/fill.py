import cv2
import numpy as np

now = datetime.now()

date = now.strftime("%d_%m_%Y-%H_%M_%S")

dt_string = "C:/Repo/opencvtests/{0}".format(date)

Path("{0}".format(dt_string)).mkdir(parents=True, exist_ok=True)

HIGH_VALUE = 10000
WIDTH = HIGH_VALUE
HEIGHT = HIGH_VALUE

cam = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cam.set(cv2.CAP_PROP_EXPOSURE, 0.05)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.mshow("test", frame)

    k = cv2.waitKey(1)

    data = {}
    dataFinal = {}
    count = 0

    if k%256 == 27:

        image = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

        #image = cv2.imread(img_name)
        #img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        #l_channel = cv2.cvtColor(img_yuv, cv2.COLOR_RGB2LUV)[:, :, 0]

        retval, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        image = cv2.dilate(image, el, iterations=1)

        cv2.imwrite("dilated.png", image)

        contours, hierarchy = cv2.findContours(
            image,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )

        s1 = 5
        s2 = 50

        drawing = cv2.imread(img_name)

        centers = []
        radii = []
        for contour in contours:
            if s1<cv2.contourArea(contour) <s2:
                area = cv2.contourArea(contour)
                if area > 100:
                    continue

                br = cv2.boundingRect(contour)
                radii.append(br[2])

                m = cv2.moments(contour)
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                centers.append(center)

        print("There are {} circles".format(len(centers)))

        radius = int(np.average(radii))

        for center in centers:
            cv2.circle(drawing, center, 1, (255, 0, 0), -1)
            #cv2.circle(drawing, center, radius, (0, 255, 0), 1)

        cv2.imwrite("drawing.png", drawing)

    elif k%256 == 32:
        img_name = "{0}opencv_frame_{1}.png".format(dt_string, img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.waitKey(0)