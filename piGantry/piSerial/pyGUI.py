import PySimpleGUI as sg
import cv2
import numpy as np

from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc


def middleWindow(motors, clearCore):

    axisOffsets = [[sg.Text("Current offset X")],[sg.InputText("0", key="offsetXOut", size=(15, 1), disabled=True)],
                   [sg.Text("Current offset Y")],[sg.InputText("0", key="offsetYOut", size=(15, 1), disabled=True)]]

    imageBlockImgL = [[sg.Text("Camera L")],[sg.Image(filename="", key="image")]]
    imageBlockImgR = [[sg.Text("Camera R")],[sg.Image(filename="", key="image2")]]
    imageRow = [sg.Column(imageBlockImgL), sg.Column(imageBlockImgR)]


    joggingElement = [[sg.Text("Number of steps to jog (e.g +6400)")],
                      [sg.InputText(key="jogXMotor", size=(15, 1)), sg.Button("Jog X motor")],
                      [sg.InputText(key="jogYMotor", size=(15, 1)), sg.Button("Jog Y motor")]]

    layout = [imageRow,
              [sg.Column(axisOffsets), sg.Column(joggingElement)],
              [sg.Button("Done")]]

    window = sg.Window("Middling setup", layout)

    cap = cv2.VideoCapture(0)


    while True:
        event, values = window.read(timeout=20)
        if (motors[0].zeroDone and motors[1].zeroDone):
            ret, frame = cap.read()
            scaleVal = 30
            height = int(frame.shape[0] * scaleVal / 100)
            width = int(frame.shape[1] * scaleVal / 100)
            dim = (width, height)

            vis = np.concatenate((frame, frame), axis=0)
            
            imgbytes = cv2.imencode(".png", cv2.resize(vis, dim, cv2.INTER_AREA))[1].tobytes()  
            window["image"].update(data=imgbytes)
            window["image2"].update(data=imgbytes)
            window["offsetXOut"].update(f"{motors[0].middleOffset}")
            window["offsetYOut"].update(f"{motors[1].middleOffset}")
            if event == "Done" or event == sg.WIN_CLOSED:
                motors[0].middleDone = True
                motors[1].middleDone = True
                break
            elif event == "Jog X motor":
                motorFunc.runOneMove(motors[0], clearCore[0], int(window["jogXMotor"].get()))
                motors[0].middleOffset += int(window["jogXMotor"].get())
            elif event == "Jog Y motor":
                motorFunc.runOneMove(motors[1], clearCore[1], int(window["jogYMotor"].get()))
                motors[1].middleOffset += int(window["jogYMotor"].get())
        else:
            sg.popup("Zero motors first!")
            break

    window.close()
def motionProfileWindow(motors):
    axisMaxTravel = [[sg.Text("X Axis max travel")],[sg.InputText("0", key="xMaxTravel", size=(15, 1), disabled=True)],
                   [sg.Text("Y Axis max travel")],[sg.InputText("0", key="yMaxTravel", size=(15, 1), disabled=True)]]
    axisStartOffset = [[sg.Text("X Axis start offset")],[sg.InputText("0", key="xstart offset", size=(15, 1), disabled=True)],
                   [sg.Text("Y Axis start offset")],[sg.InputText("0", key="ystart offset", size=(15, 1), disabled=True)]]
    setAxisMaxTravel = [[sg.Text("Set motor max travel")],
                      [sg.InputText(key="setXMaxTravel", size=(15, 1)), sg.Button("set X max travel")],
                      [sg.InputText(key="setYMaxTravel", size=(15, 1)), sg.Button("set Y max travel")]]
    setAxisPPR = [[sg.Text("Set motor pulse / revolution ratio")],
                      [sg.InputText("0", key="setPPR", size=(15, 1)), sg.Button("set p/r")]]
    stepsToMM = [[sg.Text("Convert steps to mm")], [sg.InputText("0", key="stepsToMM", size=(15, 1)), sg.Button("convert steps to mm")]]
    mmToSteps = [[sg.Text("Convert mm to steps")], [sg.InputText("0", key="mmToSteps", size=(15, 1)), sg.Button("convert mm to steps")]]

    setAxisSPM = [[sg.Text("Set motor steps per move")],
                      [sg.InputText(key="setXSPM", size=(15, 1)), sg.Button("set X steps per move")],
                      [sg.InputText(key="setYSPM", size=(15, 1)), sg.Button("set Y steps per move")]]

    conversionElements = [[setAxisPPR, stepsToMM, mmToSteps]]

    layout = [[sg.Column(axisMaxTravel),sg.Column(axisStartOffset)],
              setAxisMaxTravel,
              setAxisSPM,
              [sg.Button("Done")]]

    def paramRemainder(axis):
        param = [[sg.Text(f"{axis} axis unadjusted parameter w/ remainder")],
                  sg.Column([[sg.Text("Number of moves")], [sg.InputText("0", key=f"pR{axis}Moves", size=(15, 1), disabled=True)],
                 [sg.Text("Steps per move")],[sg.InputText("0", key=f"pR{axis}Steps", size=(15, 1), disabled=True)],
                 [sg.Text("MM per move")],[sg.InputText("0", key=f"pR{axis}StepsMM", size=(15, 1), disabled=True)]]),
                  sg.Column([[sg.Text("Travelled distance steps")],[sg.InputText("0", key=f"pR{axis}DistSteps", size=(15, 1), disabled=True)],
                  [sg.Text("Travelled distance mm")],[sg.InputText("0", key=f"pR{axis}DistMM", size=(15, 1), disabled=True)],
                 [sg.Text("Total remainder")],[sg.InputText("0", key=f"pR{axis}Remain", size=(15, 1), disabled=True)]])]
        return param

    def paramAdjusted(axis):
        param = [[sg.Text(f"{axis} axis adjusted parameter full travel")],
                  sg.Column([[sg.Text("Number of moves")], [sg.InputText("0", key=f"pA{axis}Moves", size=(15, 1), disabled=True)],
                 [sg.Text("Steps per move")],[sg.InputText("0", key=f"pA{axis}Steps", size=(15, 1), disabled=True)]])]
        return param

    paramRemainderX = paramRemainder("X")
    paramRemainderY = paramRemainder("Y")

    paramAdjustedX = paramAdjusted("X")
    paramAdjustedY = paramAdjusted("Y")


    motionOutput = [[paramRemainderX], 
                    [paramRemainderY],
                    [paramAdjustedX],
                    [paramAdjustedY]]

    window = sg.Window("Motion parameters", layout)
    windowMotor = sg.Window("Motor parameters", conversionElements)
    windowOutput = sg.Window("Motion parameters output", motionOutput)

    def setParamROut(axis):
        stepsPerMoves = int(window[f"set{axis}SPM"].get())
        numMoves = mathFunc.calcAvailableSPM(stepsPerMoves, int(motors[0].maxTravel))
        if not numMoves[0]:
            moves = numMoves[1][0]
            dist = numMoves[1][1]
            remain = numMoves[1][2]
        else:
            moves = numMoves[1]
            dist = int(motors[0].maxTravel)
            remain = "No remainder"
        windowOutput[f"pR{axis}Moves"].update(f"{moves}")
        windowOutput[f"pR{axis}Steps"].update(f"{stepsPerMoves}")
        windowOutput[f"pR{axis}StepsMM"].update(f"{mathFunc.calcDist(12800, stepsPerMoves)}")
        windowOutput[f"pR{axis}DistSteps"].update(f"{dist}")
        windowOutput[f"pR{axis}DistMM"].update(f"{mathFunc.calcDist(12800, dist)}")
        windowOutput[f"pR{axis}Remain"].update(f"{remain}")

    def setParamAOut(axis):
        stepsPerMoves = int(window[f"set{axis}SPM"].get())
        numMoves = mathFunc.calcAvailableSPM(stepsPerMoves, int(motors[0].maxTravel))
        if not numMoves[0]:
            moves = numMoves[2][0]
            steps = numMoves[2][1]
        else:
            moves = "Not applicable"
            steps = "Not applicable"
        windowOutput[f"pA{axis}Moves"].update(f"{moves}")
        windowOutput[f"pA{axis}Steps"].update(f"{steps}")


    while True:
        event, values = window.read(timeout=20)
        eventMotor, valuesMotor = windowMotor.read(timeout=20)
        eventOutput, valuesOutput = windowOutput.read(timeout=20)
        if (motors[0].middleDone and motors[1].middleDone):
            if event == "Done" or event == sg.WIN_CLOSED:
                break
            elif event == "set X max travel":
                maxVal = int(window["setXMaxTravel"].get())
                adjusted = int(maxVal + motors[0].middleOffset)
                motors[0].maxTravel = adjusted
            elif event == "set Y max travel":
                maxVal = int(window["setYMaxTravel"].get())
                adjusted = int(maxVal + motors[1].middleOffset)
                motors[1].maxTravel = adjusted
            elif event == "set X steps per move":
                setParamROut("X")
                setParamAOut("X")
            elif event == "set Y steps per move":
                setParamROut("Y")
                setParamAOut("Y")
            elif eventMotor == "set p/r":
                motors[0].pulsePerRev = int(windowMotor["setPPR"].get())
                motors[1].pulsePerRev = int(windowMotor["setPPR"].get())
            elif eventMotor == "convert steps to mm":
                mmDist = mathFunc.calcDist(motors[0].pulsePerRev, int(windowMotor["stepsToMM"].get()))
                windowMotor["stepsToMM"].update(f"{mmDist}")
            elif eventMotor == "convert mm to steps":
                stepDist = mathFunc.calcDist(motors[0].pulsePerRev, float(windowMotor["mmToSteps"].get()), convertMMToSteps=True)
                windowMotor["mmToSteps"].update(f"{stepDist}")
            window["xMaxTravel"].update(f"{motors[0].maxTravel}")
            window["yMaxTravel"].update(f"{motors[1].maxTravel}")
            windowMotor["setPPR"].update(f"{motors[0].pulsePerRev}")
        else:
            sg.popup("Complete middling first!")
            break
    
    windowMotor.close()
    windowOutput.close()
    window.close()

def mainPage(motors, micro, clearCore):
    menuDef = [["&File", ["&Load config", "&Save config", "&Exit",]],
                ["&Setup", ["&Middling", "&Motion profile"],]]
    
    motionButton = [[sg.Button("Zero X"),sg.Button("Zero Y")],
              [sg.Button("Emergency stop")]]

    layout = [[sg.Menu(menuDef)],
              [sg.Column(motionButton), sg.Output(size=(40, 10))]]

    window = sg.Window("Gantry bot", layout)

    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            break
        elif event == "Load config":
            filename = sg.popup_get_file("file to open", no_window=True)
            print(f"selected {filename}")
        elif event == "Middling":
            middleWindow(motors, clearCore)
        elif event == "Motion profile":
            motionProfileWindow(motors)
        elif event == "Zero X":
            print("Zero X started!")
            motorFunc.runZero(motors[0], (clearCore[0], micro[0]), 2)
            print("Zero X finished!")
            print(motors[0].zeroDone)
        elif event == "Zero Y":
            print("Zero Y started!")
            motorFunc.runZero(motors[1], (clearCore[1], micro[1]), 4)
            print("Zero Y finished!")
            print(motors[1].zeroDone)

#motorX = motorFunc.motor()
#motorY = motorFunc.motor()

#motorGroup = (motorX, motorY)

#mainPage(motorGroup)
#middleWindow()

#exit(0)