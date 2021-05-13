import numpy as np

class inputProcess():
    def __init__(self):
        self.steps

def calcDist(stpPerTurn, steps):
    stepPerGBTurn = float(stpPerTurn) * 20 #20 = gear ratio
    stepPerMM = float(stepPerGBTurn) / 150 #150 = mm/turn
    traveledDistMM = float(steps) / float(stepPerMM)
    return traveledDistMM
