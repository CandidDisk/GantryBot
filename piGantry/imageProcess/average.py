import cv2
import numpy as np
import json

img_name = "gray.png"

image = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

image2 = np.zeros((2448,3264,3),np.uint8)

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

print("\n\nDone\n\n")

print(len(temp2))
print(temp2[0])
print(temp2[0]["dot"][0]["row"][0])
print(temp2[0]["dot"][0]["row"][1])



for index, i in enumerate(temp2):
    rowLast = temp2[index]["dot"][len(temp2[index]["dot"])-1]["row"][0]
    rowFirst = temp2[index]["dot"][0]["row"][0]
    coords = []
    for x in temp2[index]["dot"]:
        xObj = []
        for y in x["row"]:
            try:
                xObj.append(y["col"])
                print("y col = {}".format(y["col"]))
            except:
                yVal = y
                print("y = {}".format(y))
        modObj = {"y": yVal,
                  "x": xObj}
        print(modObj)
        coords.append(modObj)

    

    dataFinal[index] = temp2[index]
    dataFinal[index]["yFirst"] = rowFirst
    dataFinal[index]["yLast"] = rowLast
    dataFinal[index]["height"] = int(rowLast - rowFirst)
    dataFinal[index]["coords"] = coords
    print(rowLast)
    print(rowFirst)
    #print(i)

with open("dataFinal.json", "w") as write_file:
    json.dump(dataFinal, write_file, indent=4)

#print(dataFinal)