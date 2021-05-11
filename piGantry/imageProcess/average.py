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

dot = False

dotCount = 1

lastRow = 0

dataFinal = {}

k = []
temp = []
temp2 = []
temp3 = []
data = {"dots": []}
count = 0

for i in range(rows):
    pointRow = {"row": [int(i)]}
    for j in range(cols):
        pixel = image[i,j]
        if (pixel != 0):
            num = count - 1
            data["dots"].append(i)
            image2[i,j] = [0,0,255]
            k.append(int(image[i,j]))
            pointObj = {
                "col": int(j),
                "val": int(pixel)
            }
            if (pointObj not in pointRow["row"]):
                pointRow["row"].append(pointObj)
            if (pointRow not in temp):
                temp.append(pointRow)
                count += 1
                try:
                    if (i - temp[num]["row"][0] <= 1):
                        if (pointRow not in temp3):
                            temp3.append(pointRow)
                    else:
                        temp3 = []
                except:
                    print()
    if (count > 0):
        try:
            obj = {
                "dot": temp3
            }
            if (obj not in temp2):
                temp2.append(obj)
            print(obj in temp2)
        except Exception as e:
            print(e)

with open("data.json", "w") as write_file:
    json.dump(temp2, write_file, indent=4)

cv2.imwrite("image2.png", image2)



for index, i in enumerate(temp2):
    colLast = 0
    colFirst = 0
    rowLast = temp2[index]["dot"][len(temp2[index]["dot"])-1]["row"][0]
    rowFirst = temp2[index]["dot"][0]["row"][0]
    coords = []
    for x in temp2[index]["dot"]:
        xObj = []
        firstCol = x["row"][1]["col"]
        lastCol = x["row"][len(x["row"])-1]["col"]
        print(len(x["row"]))
        print(x["row"])
        if (colLast == 0 and colFirst == 0):
            colLast = lastCol
            colFirst = firstCol
        else:
            if (firstCol < colFirst):
                colFirst = firstCol
            if (lastCol > colLast):
                colLast = lastCol
        for y in x["row"]:
            try:
                xObj.append(y["col"])
            except:
                yVal = y
        modObj = {"y": yVal,
                  "x": xObj}
        coords.append(modObj)
    
    centreObj = {"x": int((colFirst + colLast)/2),
                 "y": int((rowFirst + rowLast)/2)}

    dataFinal[index] = temp2[index]
    dataFinal[index]["yFirst"] = rowFirst
    dataFinal[index]["yLast"] = rowLast
    dataFinal[index]["xFirst"] = colFirst
    dataFinal[index]["xLast"] = colLast
    dataFinal[index]["centre"] = centreObj
    dataFinal[index]["height"] = int(rowLast - rowFirst)
    dataFinal[index]["coords"] = coords
    cv2.circle(image3,(centreObj["x"],centreObj["y"]), 1, (0,0,255), -1)

cv2.imwrite("image3.png", image3)

with open("dataFinal.json", "w") as write_file:
    json.dump(dataFinal, write_file, indent=4)
