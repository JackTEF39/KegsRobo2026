from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *
from Helpers import *
#from AcidStrategy import *
#from BaseStrategy import *

robot = Robot()
markerIDs["home"] = getHomeMarkerIds(robot)

CAMHEIGHT = 120 #height of the camera from the ground in metres
#CAMANGLE = 20 #angle of the camera to the ground in degrees

#Motor control:
#700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

my_motor_board = robot.motor_board      #declarations
my_arduino_board = robot.arduino
my_power_board = robot.power_board

servo1 = robot.servo_board.servos[0]
servo2 = robot.servo_board.servos[1]
servoTop = robot.servo_board.servos[2]

robot.arduino.pins[3].mode = INPUT_PULLUP # Encoder inputs need to be pullup or the motor won't run (learnt the hard way)
robot.arduino.pins[2].mode = INPUT_PULLUP
robot.arduino.pins[5].mode = INPUT_PULLUP
robot.arduino.pins[4].mode = INPUT_PULLUP



def initialise():
    marker = findTargetMarker(robot)
    if marker is not None:
        if marker.id in range(20):
            print("Arena marker found")
        elif marker.id in range(100, 140):
            print("Acid marker found")
            collecting = "acid"                 #Store the type of marker we are collecting so we can check if we are collecting the right one later (doesnt matter for now)
        elif marker.id in range(140, 180):
            print("Base marker found")
            collecting = "base"
    my_home_ids = getHomeMarkerIds(robot)

def arduinoSet(pin, outState): #self explanatory.
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(pin): #self explanatory.
    return robot.arduino.pins[pin].digital_read()

def moveWithChecks(robot, distance, targetId):
    total_steps = int(distance * STEPS_PER_MM)
    for i in range(0, total_steps):
        stepMotorsForward(robot, 1)
        alignToTarget(robot, targetId) # Check alignment after every step and adjust if necessary
        robot.sleep(0.01)

def visionMvnmtTest1():                          #isolated vision and mvnmt test no checks
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = horDistCalculate(target)
    print(f"Distance to target: {dist}m")
    stepMotorsForward(robot, 2000)

def alignCheck():                      #vision and mvnmt test with checks
    target = findTargetMarker(robot)
    print(f"Target {target.id} found. Aligning")
    alignToTarget(robot, target)

def visionMvnmtTest2():                      #vision and mvnmt test with checks
    target = findTargetMarker(robot)
    print(f"Target {target.id} found. Aligning")
    alignToTarget(robot, target)
    dist = horDistCalculate(target)
    print(f"Distance to target: {dist}m")
    moveWithChecks(robot, dist -100, target.id)

def fullSysTest():                              #vision mvmnt + mechanism test
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = horDistCalculate(target)
    mechanismOpen(robot, servo1, servo2)
    print(f"Distance to target: {dist}m")
    stepMotorsForward(robot, 2000)
    mechanismClose(robot, servo1, servo2)

# ---MAIN LOOP--- 
                                                        ###############
startTime = robot.time()
endTime = 0
duration = 0

indicatePowerOn(robot)
sweep(robot, servoTop)
mechanismClose(robot, servo1, servo2)
print("Starting...")
targ_id = findTargetMarker(robot, COLLECTING_PH).id # might give error if doesn't see marker, but it alr lined up at start so should be fine
aligned = False

# Start - go to first marker (assumed straight on)
obtainedMarker = obtainMarker(robot, targ_id, servo1, servo2)

if obtainedMarker:
    markerIDsAcquired.append(targ_id)
print(markerIDsAcquired)

endTime = robot.time()
duration = endTime - startTime

if MATCH_DURATION - duration > ABORT_THRESHOLD:
    # Find second marker
    final_targ = findTargetMarker(robot, COLLECTING_PH)
    targ_id = findTargetMarker(robot, COLLECTING_PH).id
    aligned = alignToTarget(robot, targ_id)

    obtainedMarker = obtainMarker(robot, targ_id, servo1, servo2) 

    if obtainedMarker:
        markerIDsAcquired.append(targ_id)
    print(markerIDsAcquired)

returnToHome(robot) # goes home

# deposit
mechanismOpen(robot, servo1, servo2)
stepMotors(-900)

endTime = robot.time()
duration = endTime - startTime

if MATCH_DURATION - duration > ABORT_THRESHOLD:
    # Go for the top boxes next
    stepMotorsRotate(robot, convertAngToSteps(180)) # face the middle

    targ_id = findTargetMarker(robot, COLLECTING_PH, True).id
    aligned = alignToTarget(robot, targ_id)

    obtainedMarker = obtainMarkerTop(robot, targ_id, servo1, servo2, servoTop)

    if obtainedMarker:
            markerIDsAcquired.append(targ_id)
    print(markerIDsAcquired)

    returnToHome(robot) # goes home
