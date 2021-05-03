import sys
import json 

json1 = "dataFinal_file.json"
json2 = "dataFinal_file1.json"

with open(json1) as json_file:
    data1 = json.load(json_file)

with open(json2) as json_file:
    data2 = json.load(json_file)

xSame = 0
ySame = 0
xySame = 0

#for key, value in data1.items():
#    print(key)
#    print(value.get('width'))
#    print(value.get('height'))
#    print("end")
#print("ended data 1")
#for key, value in data2.items():
#    print(key)
#    print(value.get('width'))
#    print(value.get('height'))
#    print("end")
#print("ended data 2")

for key in data1.items():
    print("start")
    print(key[0])
    print("data1")
    print(data1["{}".format(key[0])]['x'])
    print(data1["{}".format(key[0])]['y'])
    print("data2")
    print(data2["{}".format(key[0])]['x'])
    print(data2["{}".format(key[0])]['y'])
    print("end\n")

    if (data1["{}".format(key[0])]['x'] == data2["{}".format(key[0])]['x']
        and data1["{}".format(key[0])]['y'] == data2["{}".format(key[0])]['y']):
        xySame += 1
    elif (data1["{}".format(key[0])]['y'] == data2["{}".format(key[0])]['y']):
        ySame += 1
    elif (data1["{}".format(key[0])]['x'] == data2["{}".format(key[0])]['x']):
        xSame += 1

print(xySame)
print(ySame)
print(xSame)
        



