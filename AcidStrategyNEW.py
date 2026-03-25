from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *

def getFirstAcid(): # Values may not be perfect - CHECK ON WEDS
    robot = Robot()
    initialSteps = distanceToSteps(1325) #1325mm is distance from Robot lined up to centre of nearest Acid marker
    stepMotorsForward(initialSteps)
    mechanismOpen()
    stepMotorsRotate(robot, (DEG10 * 9))
    initialStepsTurn = distanceToSteps(455) #455mm is rough distance to centre of marker
    mechanismClose()
