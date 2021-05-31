import cv2
import numpy as np
from matplotlib import pyplot as plt

class inputProcess():
    def __init__(self):
        self.steps

# Converts steps to mm given pulses/revolution & number of steps
def calcDist(stpPerTurn, steps):
    stepPerGBTurn = float(stpPerTurn) * 20 #20 = gear ratio
    stepPerMM = float(stepPerGBTurn) / 150 #150 = mm/turn
    traveledDistMM = float(steps) / float(stepPerMM)
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
