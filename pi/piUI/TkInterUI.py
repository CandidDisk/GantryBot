#Redundant import for sake of testing
from tkinter import *

import tkinter as tk

import math

class pointConfigUI(object):
    def __init__(self, master):

        top = tk.Toplevel()
        top.geometry("800x280+10+10")

        self.xAxisPoints = 0
        self.yAxisPoints = 1

        self.intervDistFinalX = 0
        self.pointCountFinalX = 0
        self.totalDistFinalX = 0

        self.intervDistFinalY = 0
        self.pointCountFinalY = 0
        self.totalDistFinalY = 0

        self.top = top
        self.l=Label(top, text="Distance for X axis")
        self.l.place(x=30, y=20)
        self.eX1=Entry(top)
        self.eX1.place(x=200, y=20)

        self.l=Label(top, text="Num. of points X axis")
        self.l.place(x=30, y=60)
        self.eX2=Entry(top)
        self.eX2.place(x=200, y=60)

        self.b=Button(top,text='Submit X values',command= lambda: self.cleanup(self.xAxisPoints))
        self.b.place(x=30, y=100)

        self.l=Label(top, text="Distance for Y axis")
        self.l.place(x=30, y=140)
        self.eY1=Entry(top)
        self.eY1.place(x=200, y=140)

        self.l=Label(top, text="Num. of points Y axis")
        self.l.place(x=30, y=180)
        self.eY2=Entry(top)
        self.eY2.place(x=200, y=180)

        self.b=Button(top,text='Submit Y values',command=lambda: self.cleanup(self.yAxisPoints))
        self.b.place(x=30, y=220)

        self.Console = Text(top, height=10, width=50)
        self.Console.place(x=350, y=20)
        self.scroll = tk.Scrollbar(top, command=self.Console.yview)
        self.Console.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        Label(top, text="X - ", font=('Helvetica', 10)).place(x=350, y= 210)
        Label(top, text="Y - ", font=('Helvetica', 10)).place(x=348, y= 240)

        Label(top, text="Num. of points", font=('Helvetica', 10)).place(x=390, y= 190)
        Label(top, text="Total Distance", font=('Helvetica', 10)).place(x=520, y= 190)
        Label(top, text="Interval Dist.", font=('Helvetica', 10)).place(x=650, y= 190)

        self.valuesX = {'points': {'value': self.pointCountFinalX,
                                 'var': StringVar()},
                    'total': {'value': self.totalDistFinalX,
                                 'var': StringVar()},
                    'dist': {'value': self.intervDistFinalX,
                                 'var': StringVar()}}

        self.valuesY = {'points': {'value': self.pointCountFinalY,
                                 'var': StringVar()},
                    'total': {'value': self.totalDistFinalY,
                                 'var': StringVar()},
                    'dist': {'value': self.intervDistFinalY,
                                 'var': StringVar()}}

        self.valuesXLabels = {}
        self.valuesYLabels = {}


        xPos = 392

        for (text, value) in self.valuesX.items():
            value['var'].set(value['value'])

            self.valuesXLabels[text] = Label(top, textvariable = value['var'], font=('Helvetica', 10), height = 1, width = 10, borderwidth = 2, relief = "sunken")
            
            self.valuesXLabels[text].place(x=xPos, y= 210)
            xPos += 130
        xPos = 392

        for (text, value) in self.valuesY.items():
            value['var'].set(value['value'])

            self.valuesYLabels[text] = Label(top, textvariable = value['var'], font=('Helvetica', 10), height = 1, width = 10, borderwidth = 2, relief = "sunken")
            
            self.valuesYLabels[text].place(x=xPos, y= 240)
            xPos += 130



    def cleanup(self, axis):
        self.values = {
            'valueDistX': self.eX1.get(),
            'valueNumX': self.eX2.get(),
            'valueDistY': self.eY1.get(),
            'valueNumY': self.eY2.get()
        }
        
        if (axis == 0):
            axis = stepResolv(self.eX1.get(), self.eX2.get())
            axisName = "X Axis"
            values = self.valuesX
        elif (axis == 1):
            axis = stepResolv(self.eY1.get(), self.eY2.get())
            axisName = "Y Axis"
            values = self.valuesY
            
        #if (not xAxisPoints['valid']):
        #    windowTemp = Tk() 
        #    windowTemp.geometry('100x150') 

        #    btnPCU = Button(windowTemp, text=xAxisPoints['pointCountUp'])
        #    btnPCU.pack()

        #    btnPCD = Button(windowTemp, text=xAxisPoints['pointCountDown'])
        #    btnPCD.pack()

        #Console = Text(windowTemp)

        
        #Console.pack()
        
        text = "==========\n\nCurrent {} values: \n\nPoints: {}\nTotal distance: {}\nInterval distance: {}\n\nRecommended {} Values: \n\n".format(axisName, axis['uncorrectedPointCount'], axis['uncorrectedDist'], axis['intervDist'], axisName)

        #radioText = {}

        self.Console.insert(INSERT,  text)

        for key in axis['pointCounts']:
            points =  axis['pointCounts'][key]['points']
            total = axis['pointCounts'][key]['total']
            dist = axis['pointCounts'][key]['dist']

            text = "Set: {} \nPoints: {}\nTotal distance: {}\nInterval distance: {}\n\n".format(key, points, total, dist)

            self.Console.insert(INSERT, text)


        windowTemp = Tk()
        windowTemp.geometry('200x175')

        var = IntVar()

        Radiobutton(windowTemp, text="Current {} value".format(axisName), variable = var, value = 1, background = "light blue", indicator = 0, command = lambda: setFinalValues(axis, "uncorrectedPoints", values)).pack(fill = X, ipady = 5)

        Radiobutton(windowTemp, text="pointCountUpCeil", variable = var, value = 2, background = "light blue", indicator = 0, command = lambda: setFinalValues(axis, "pointCountUpCeil", values)).pack(fill = X, ipady = 5)

        Radiobutton(windowTemp, text="pointCountDownCeil", variable = var, value = 3, background = "light blue", indicator = 0, command = lambda: setFinalValues(axis, "pointCountDownCeil", values)).pack(fill = X, ipady = 5)

        Radiobutton(windowTemp, text="pointCountUpFloor", variable = var, value = 4, background = "light blue", indicator = 0, command = lambda: setFinalValues(axis, "pointCountUpFloor", values)).pack(fill = X, ipady = 5)

        Radiobutton(windowTemp, text="pointCountDownFloor", variable = var, value = 5, background = "light blue", indicator = 0, command = lambda: setFinalValues(axis, "pointCountDownFloor", values)).pack(fill = X, ipady = 5)

        

        def setFinalValues(axis, selection, itemValues):
            for (value) in itemValues:
                itemValues[value]['var'].set(axis['pointCounts'][selection][value])


        #self.top.destroy()

class mainUI(object):
    def __init__(self, master):
        self.master = master

        self.Console = Text(master, height=15, width=50)
        self.Console.place(x=350, y=20)
        self.scroll = tk.Scrollbar(master, command=self.Console.yview)
        self.Console.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.xYBtn=Button(master, text="Setup number of x/y positions", command = self.popup)
        self.xYBtn.place(x=30, y=20)

        self.zBtn=Button(master, text="Set zero")
        self.zBtn.place(x=30, y=60)

        self.eBtn=Button(master, text="Emergency Stop", fg="red")
        self.eBtn.place(x=30, y=100)

        self.camLbl=Label(master, text="Camera pixel compensation", font=("Helvetica", 10))
        self.camLbl.place(x=30, y=140)
        
        self.cam1Lbl=Label(window, text="Left camera", font=("Helvetica", 10))
        self.cam1Lbl.place(x=60, y=180)
        
        self.cam2Lbl=Label(window, text="Right camera", font=("Helvetica", 10))
        self.cam2Lbl.place(x=60, y=220)

        self.cameraCompTxtL=Entry(window)
        self.cameraCompTxtL.place(x=180, y=180)

        self.cameraCompTxtR=Entry(window)
        self.cameraCompTxtR.place(x=180, y=220)

    def popup(self):
        self.w=pointConfigUI(self.master)
        self.xYBtn["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.xYBtn["state"] = "normal"

    def entryValue(self):
        return self.w.values

def stepResolv(total: float, pointCount: int):
    newPointCount = int(pointCount)
    intervDist = round(float(total) / int(newPointCount), 2)
    uncorrectedPointCount = round((float(total) / intervDist), 0)
    uncorrectedDist = (uncorrectedPointCount) * intervDist 

    roundUp = math.ceil(intervDist)
    roundDown = math.floor(intervDist)

    values = {
        'intervDistFinal': 0,
        'intervDist': intervDist,
        'pointCountFinal': pointCount,
        'uncorrectedPointCount': uncorrectedPointCount,
        'uncorrectedDist': uncorrectedDist,
        'valid': FALSE,
        'roundUp': roundUp,
        'roundDown': roundDown,
        'pointCounts': {
            'uncorrectedPoints': {
                'points': uncorrectedPointCount,
                'total': uncorrectedDist,
                'dist': intervDist
            },
            'pointCountUpCeil': {
                'points': math.ceil((float(total) / roundUp) - 1),
                'total': (math.ceil((float(total) / roundUp) - 1)) * roundUp,
                'dist': roundUp
            },
            'pointCountDownCeil': {
                'points': math.ceil((float(total) / roundDown) - 1),
                'total': (math.ceil((float(total) / roundDown) - 1)) * roundDown,
                'dist': roundDown
            },
            'pointCountUpFloor': {
                'points': math.floor((float(total) / roundUp) - 1),
                'total': (math.floor((float(total) / roundUp) - 1)) * roundUp,
                'dist': roundUp
            },
            'pointCountDownFloor': {
                'points': math.floor((float(total) / roundDown) - 1),
                'total': (math.floor((float(total) / roundDown) - 1)) * roundDown,
                'dist': roundDown
            }
        }
    }

    if (uncorrectedPointCount*intervDist <= 100):
        values['valid'] = TRUE
        values['intervDistFinal'] = intervDist

    return values



window = Tk()
window.title('Hello Python')
window.geometry("800x300+10+10")



m = mainUI(window)
window.mainloop()

