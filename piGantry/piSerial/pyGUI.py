import PySimpleGUI as sg
import cv2
import numpy as np

from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc

class uiSTATE():
    def __init__(self, debugMode = False):
        self.debugMode = debugMode

    def middleWindow(self, motors, clearCore):
        topDot = (1200,100)
        topDotM = (1210,100)

        # Initializes cam 0, 1 w/o cam object
        # Will refactor to use proper cameraFunc object
        cap = cv2.VideoCapture(0) # Cam 0
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        cap2 = cv2.VideoCapture(1) # Cam 1
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

        axisOffsets = [[sg.Text("Top dot difference")],[sg.Text("0", key="offsetXOut", size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Bottom dot difference")],[sg.Text("0", key="offsetYOut", size=(13, 1), relief="sunken", border_width=None,  background_color="gray")]]

        dotCoords = [[sg.Text("Top dot coords")],[sg.Text("0", key="dotCoordsT", size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Bottom dot coords")],[sg.Text("0", key="dotCoordsB", size=(13, 1), relief="sunken", border_width=None,  background_color="gray")]]

        dotCoordsM = [[sg.Text("Top dot mirror coords")],[sg.Text("0", key="dotCoordsTM", size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Bottom dot mirror coords")],[sg.Text("0", key="dotCoordsBM", size=(13, 1), relief="sunken", border_width=None,  background_color="gray")]]

        imageBlockImgL = [[sg.Text("Camera L")],[sg.Image(filename="", key="image")]]
        imageBlockImgR = [[sg.Text("Camera R")],[sg.Image(filename="", key="image2")]]
        imageRow = [sg.Column(imageBlockImgL), sg.Column(imageBlockImgR)]
        #coordRow = [sg.Column(dotCoords), sg.Column(dotCoordsM)]


        joggingElement = [[sg.Text("Number of steps to jog (e.g +6400)")],
                        [sg.InputText(key="jogXMotor", size=(13, 1)), sg.Button("Jog X motor")],
                        [sg.InputText(key="jogYMotor", size=(13, 1)), sg.Button("Jog Y motor")]]

        layout = [imageRow,
                [sg.Column(axisOffsets), sg.Column(dotCoords), sg.Column(dotCoordsM), sg.Column(joggingElement), sg.Output(size=(40, 10))],
                [sg.Button("Done")]]

        window = sg.Window("Middling setup", layout)




        while True:
            event, values = window.read(timeout=20)
            if (motors[0].zeroDone and motors[1].zeroDone or self.debugMode):
                ret, frame = cap.read()
                ret2, frame2 = cap2.read()
                cv2.circle(frame, topDot, 10, (255,0,0), -1)
                cv2.circle(frame2,topDotM, 10, (255,0,0), -1)
                frame2 = cv2.flip(frame2, 1)

                #cv2.line(frame,(0,0),(511,511),(255,0,0),5)
                scaleVal = 23
                height = int(frame.shape[0] * scaleVal / 100)
                width = int(frame.shape[1] * scaleVal / 100)
                dim = (width, height)
                #vis = np.concatenate((frame, frame), axis=0)
                
                imgbytes = cv2.imencode(".png", cv2.resize(frame, dim, cv2.INTER_AREA))[1].tobytes()  
                imgbytes2 = cv2.imencode(".png", cv2.resize(frame2, dim, cv2.INTER_AREA))[1].tobytes()  
                window["image"].update(data=imgbytes)
                window["image2"].update(data=imgbytes2)
                window["offsetXOut"].update(f"{motors[0].middleOffset}")
                window["offsetYOut"].update(f"{motors[1].middleOffset}")
                if event == "Done" or event == sg.WIN_CLOSED:
                    motors[0].middleDone = True
                    motors[1].middleDone = True
                    break
                elif event == "Jog X motor":
                    if (not self.debugMode):
                        motorFunc.runOneMove(motors[0], clearCore[0], int(window["jogXMotor"].get()))
                    motors[0].middleOffset += int(window["jogXMotor"].get())
                elif event == "Jog Y motor":
                    if (not self.debugMode):
                        motorFunc.runOneMove(motors[1], clearCore[1], int(window["jogYMotor"].get()))
                    motors[1].middleOffset += int(window["jogYMotor"].get())
            else:
                sg.popup("Zero motors first!")
                break

        window.close()
    def motionProfileWindow(self, motors):
        axisMaxTravel = [[sg.Text("X Axis max travel")],[sg.Text("0", key="xMaxTravel", size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Y Axis max travel")],[sg.Text("0", key="yMaxTravel",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]
        axisStartOffset = [[sg.Text("X Axis start offset")],[sg.Text("0", key="xstart offset",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Y Axis start offset")],[sg.Text("0", key="ystart offset",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]
        setAxisMaxTravel = [[sg.Text("Set motor max travel")],
                        [sg.InputText(key="setXMaxTravel", size=(13, 1)), sg.Button("set X max travel")],
                        [sg.InputText(key="setYMaxTravel", size=(13, 1)), sg.Button("set Y max travel")]]
        setAxisPPR = [[sg.Text("Set motor pulse / revolution ratio")],
                        [sg.InputText("0", key="setPPR", size=(13, 1)), sg.Button("set p/r")],
                        [sg.Text("Current motor pulse / revolution ratio")], [sg.Text("0", key="showPPR", size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]
        stepsToMM = [[sg.Text("Convert steps to mm")], [sg.InputText("0", key="stepsToMM", size=(13, 1)), sg.Button("convert steps to mm")], [sg.Text("0", key="showStepsToMM", size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]
        mmToSteps = [[sg.Text("Convert mm to steps")], [sg.InputText("0", key="mmToSteps", size=(13, 1)), sg.Button("convert mm to steps")],  [sg.Text("0", key="showMmToSteps", size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]

        setAxisSPM = [[sg.Text("Set motor steps per move")],
                        [sg.InputText(key="setXSPM", size=(13, 1)), sg.Button("set X steps per move")],
                        [sg.InputText(key="setYSPM", size=(13, 1)), sg.Button("set Y steps per move")]]

        conversionElements = [[setAxisPPR, stepsToMM, mmToSteps]]

        layout = [[sg.Column(axisMaxTravel),sg.Column(axisStartOffset)],
                setAxisMaxTravel,
                setAxisSPM,
                [sg.Button("Done")]]

        def paramRemainder(axis):
            param = [[sg.Text(f"{axis} axis unadjusted parameter w/ remainder")],
                    sg.Column([[sg.Text("Number of moves")], [sg.Text("0", key=f"pR{axis}Moves",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Steps per move")],[sg.Text("0", key=f"pR{axis}Steps",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("MM per move")],[sg.Text("0", key=f"pR{axis}StepsMM",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")]]),
                    sg.Column([[sg.Text("Travelled distance steps")],[sg.Text("0", key=f"pR{axis}DistSteps",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Travelled distance mm")],[sg.Text("0", key=f"pR{axis}DistMM",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Total remainder")],[sg.Text("0", key=f"pR{axis}Remain",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")]])]
            return param

        def paramAdjusted(axis):
            param = [[sg.Text(f"{axis} axis adjusted parameter full travel")],
                    sg.Column([[sg.Text("Number of moves")], [sg.Text("0", key=f"pA{axis}Moves",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")],
                    [sg.Text("Steps per move")],[sg.Text("0", key=f"pA{axis}Steps",  size=(13, 1), relief="sunken", border_width=None, background_color="gray")]])]
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
            if (motors[0].middleDone and motors[1].middleDone or self.debugMode):
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
                    windowMotor["showStepsToMM"].update(f"{mmDist}")
                elif eventMotor == "convert mm to steps":
                    stepDist = mathFunc.calcDist(motors[0].pulsePerRev, float(windowMotor["mmToSteps"].get()), convertMMToSteps=True)
                    windowMotor["showMmToSteps"].update(f"{stepDist}")
                window["xMaxTravel"].update(f"{motors[0].maxTravel}")
                window["yMaxTravel"].update(f"{motors[1].maxTravel}")
                windowMotor["showPPR"].update(f"{motors[0].pulsePerRev}")
            else:
                sg.popup("Complete middling first!")
                break
        
        windowMotor.close()
        windowOutput.close()
        window.close()

    def mainPage(self, motors, micro, clearCore):
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
                self.middleWindow(motors, clearCore)
            elif event == "Motion profile":
                self.motionProfileWindow(motors)
            elif event == "Zero X":
                print("Zero X started!")
                if (not self.debugMode):
                    motorFunc.runZero(motors[0], (clearCore[0], micro[0]), 2)
                else:
                    motors[0].zeroDone = True
                print("Zero X finished!")
                print(motors[0].zeroDone)
            elif event == "Zero Y":
                print("Zero Y started!")
                if (not self.debugMode):
                    motorFunc.runZero(motors[1], (clearCore[1], micro[1]), 4)
                else:
                    motors[1].zeroDone = True
                print("Zero Y finished!")
                print(motors[1].zeroDone)

#motorX = motorFunc.motor()
#motorY = motorFunc.motor()

#motorGroup = (motorX, motorY)

#mainPage(motorGroup)
#middleWindow()

#exit(0)