import cv2
import numpy as np
from matplotlib import pyplot as plt

class inputProcess():
    def __init__(self):
        self.steps

# Converts steps to mm given pulses/revolution & number of steps
def calcDist(stpPerTurn, unit, convertMMToSteps=False):
    stepPerGBTurn = float(stpPerTurn) * 20 #20 = gear ratio
    stepPerMM = float(stepPerGBTurn) / 150 #150 = mm/turn
    
    if convertMMToSteps:
        traveledDistSteps = float(unit) * float(stepPerMM)
        return traveledDistSteps
    else:
        traveledDistMM = float(unit) / float(stepPerMM)
        return traveledDistMM

# Solves & plots best fit given x,y center points
def bestFitPoly(xList, yList, deg, imgOrig):
    imgRotate = cv2.rotate(imgOrig, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.flip(imgRotate, 0)
    fig, ax = plt.subplots()
    # Plot as inverse
    coefs = np.polyfit(xList, yList, deg)
    ax.imshow(img)
    ax.plot(xList, yList, 'o')#linewidth=1)
    coefsPoly = np.poly1d(coefs)
    ax.plot(xList, coefsPoly(xList))
    plt.show()

def calcAvailableSPM(stpPerTurn, totalDist):
    numMoves = float(int(totalDist) / int(stpPerTurn))
    if (numMoves).is_integer():
        return (True, numMoves)
    else:
        newNumMoves = numMoves
        newStpPerTurn = stpPerTurn
        travelDist = int(int(totalDist) // int(stpPerTurn) * stpPerTurn)
        remainder = int(totalDist) % int(stpPerTurn)
        while not (newNumMoves).is_integer():
            newStpPerTurn += 1
            newNumMoves = float(int(totalDist) / int(newStpPerTurn))
        return (False, (round(numMoves), travelDist, remainder), (newNumMoves, newStpPerTurn))

