import cv2
import numpy as np
import json

img_name = "gray.png"

image = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

image2 = np.zeros((2448,3264,3),np.uint8)
image3 = np.zeros((2448,3264,3),np.uint8)

retval, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

image = cv2.dilate(image, el, iterations=1)

cv2.imwrite("dilatedAvg.png", image)

rows,cols = image.shape

refDot = []
dataFinal = []
dotArr = []

count = 0
prevLength = 0

for i in range(rows):
    pointRow = {"row": int(i),
                "col": []}
    for j in range(cols):
        pixel = image[i,j]
        if (pixel != 0):
            num = count - 1
            image2[i,j] = [0,0,255]

            if (int(j) not in pointRow["col"]):
                pointRow["col"].append(int(j))
            if (pointRow not in refDot):
                refDot.append(pointRow)
                count += 1
                try:
                    if (i - refDot[num]["row"] <= 1):
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
                    rowFirst = dotArr[0]["row"]
                    try:
                        rowLast = dotArr[len(dotArr)-1]["row"]                        
                    except:
                        continue
                    for i in dotArr:
                        lastVal = i["col"][len(i["col"])-1]
                        firstVal = i["col"][0]
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
        except Exception as e:
            continue
        
with open("data.json", "w") as write_file:
    json.dump(dataFinal, write_file, indent=4)
