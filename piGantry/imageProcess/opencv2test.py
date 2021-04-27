import cv2
import sys
import numpy as np
import math
import json
from pathlib import Path
from datetime import datetime

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
cam.set(cv2.CAP_PROP_EXPOSURE, 10)

cv2.namedWindow("test")

img_counter = 0



while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        image = cv2.imread(img_name)
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(img_yuv)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        l_channel = cv2.cvtColor(img_yuv, cv2.COLOR_RGB2LUV)[:, :, 0]
        cv2.imwrite('{0}/l_channel.png'.format(dt_string), l_channel)
        cv2.imwrite('{0}/y.png'.format(dt_string), img_yuv)
        cv2.imwrite('{0}/u.png'.format(dt_string), img_yuv)
        cv2.imwrite('{0}/v.png'.format(dt_string), img_yuv)
        cv2.imwrite('{0}/yuv.png'.format(dt_string), img_yuv)
        
        cv2.imwrite('{0}/grey.png'.format(dt_string), gray)
        thresh = cv2.threshold(l_channel, 5, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Filter out large non-connecting objects
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        print(cnts)


        #cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #for c in cnts:
        #    area = cv2.contourArea(c)
        #    if area < 500:
        #        cv2.drawContours(thresh,[c],0,0,-1)

        # Morph open using elliptical shaped kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

        # Find circles 
        #cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #for c in cnts:
        #    area = cv2.contourArea(c)
        #    if area > 20 and area < 50:
        #        ((x, y), r) = cv2.minEnclosingCircle(c)
        #        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

        s1 = 20
        s2 = 500
        xcnts = []
        data = {}
        dataFinal = {}
        count = 0

        tempCenterX = 0
        tempCenterY = 0

        for cnt in cnts:
            print(cnts[2]/[3])
            if s1<cv2.contourArea(cnt) <s2:
                count += 1
                print("cnt = {0}, count = {1} ".format(cnt, count))
                

                x, y, w, h = cv2.boundingRect(cnt)


                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print("width = {0} ".format(w))
                print("height = {0} ".format(h))


                #rect = cv2.minAreaRect(cnt)
                #box = cv2.boxPoints(rect)

                #box = np.int0(box)
                #cv2.drawContours(image, [box], 0, (0, 0, 255))

                #blank_image = np.zeros(gray.shape, np.uint8)

                #cv2.drawContours(blank_image, [box], 0, (0, 0, 255))

                #covers contour w/ a circle covering minimum area
                (x2, y2), radius = cv2.minEnclosingCircle(cnt)

                print(x)
                print(y)

                print(int(x2), int(y2))

                intensity = l_channel[int(y2)][int(x2)]

                print("l_channel = {0} ".format(intensity))

                center = (int(x2), int(y2))

                radius = int(radius*0.25)

                distPrevious = math.sqrt((x2-tempCenterX)**2+(y2-tempCenterY)**2)

                #distPrevious = sqrt((x2-tempCenterX)^2+(y2-tempCenterY)^2) )

                print("distance to previous point = {0} ".format(distPrevious))

                print("center = {0} ".format(center))

                print("radius = {0} ".format(radius))
                

                imgBound = cv2.circle(image, center, radius, (255, 0, 0), 2)

                #mask_contour = blank_image == 255
                
                #intensity = np.mean(gray[mask_contour])

                #print("intensity = {0} ".format(intensity))

                dataContour = {
                    int(count): {
                        "center": center,
                        "width": w,
                        "height": h,
                        "radius": radius,
                        "intensity": int(intensity),
                        "x": x,
                        "y": y,
                        "distPrevious": distPrevious,
                        "distNext": 0,
                        "distDiff": 0
                    }

                }
                data.update(dataContour)
                xcnts.append(cnt)
                tempCenterX = x2
                tempCenterY = y2
        
        #print(data)
        for key, value in data.items():

            next = key + 1
            prev = key - 1

            x1 = data.get(key).get('center')[0]
            y1 = data.get(key).get('center')[1]

            if key != count:

                x2 = data.get(next).get('center')[0]
                y2 = data.get(next).get('center')[1]

                distNext = math.sqrt((x2-x1)**2+(y2-y1)**2)

                data[key]['distNext'] = distNext
                
                if key != 1:
                    distDiff = distNext - data[prev]['distNext']
                    data[prev]['distDiff'] = distDiff


                #data.get(key).get('distNext') = distNext

        count = 0

        for key, value in data.items():

            if -10 < data[key]['distDiff'] < 10:
                count += 1
                dataFinal[count] = value
                



        #print(data.get(1).get('center')[0])
        #print(data.get(1).get('center')[1])

        #print(data.get(2).get('center')[0])
        #print(data.get(2).get('center')[1])

        #print(data)

        #print(len(xcnts))

        #cv2.imshow("Image", blank_image)

        #print(cnts)

        cv2.drawContours(imgBound, xcnts, -1, (255, 255, 0), 1)

        #cv2.imshow("contours", imgBound)
        

        #cv2.imshow('thresh', thresh)
        #cv2.imshow('opening', opening)
        #cv2.imshow('image', image)
        
        #print("\nDots number: {}".format(count))


        with open("{0}/data_file.json".format(dt_string), "w") as write_file:
            json.dump(data, write_file, indent=4)

        with open("{0}/dataFinal_file.json".format(dt_string), "w") as write_file:
            json.dump(dataFinal, write_file, indent=4)
        
        cv2.imwrite("{0}/contours.png".format(dt_string), imgBound)
        cv2.imwrite("{0}/thresh.png".format(dt_string), thresh)
        cv2.imwrite("{0}/opening.png".format(dt_string), opening)
        cv2.imwrite("{0}/image.png".format(dt_string), image)

        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{0}opencv_frame_{1}.png".format(dt_string, img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1


cam.release()

# Load image, grayscale, Otsu's threshold


cv2.waitKey(0)

#contigious pixels (cant skip more than 1 or 2 blank pixel x/y), 