# UPDATED COMP CODE - 24.03.2026
from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *

robot = Robot()

CAMHEIGHT = 120 #height of the camera from the ground in metres
#CAMANGLE = 20 #angle of the camera to the ground in degrees
STEPS_PER_MM = 2.476 #How far the robot moves per step of the motor (in mm)

#Motor control:
#700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

my_motor_board = robot.motor_board      #declarations
my_arduino_board = robot.arduino
my_servo_board = robot.servo_board
my_power_board = robot.power_board

servo1 = robot.servo_board.servos[0]
servo2 = robot.servo_board.servos[1]

robot.arduino.pins[3].mode = INPUT_PULLUP # Encoder inputs need to be pullup or the motor won't run (learnt the hard way)
robot.arduino.pins[2].mode = INPUT_PULLUP
robot.arduino.pins[5].mode = INPUT_PULLUP
robot.arduino.pins[4].mode = INPUT_PULLUP

def getHomeMarkerIds(robot):
    z = robot.zone 
    zone_map = {
        0: (0, 18, 19),    
        1: (3, 4, 5),    
        2: (8, 9, 10), 
        3: (13, 14, 15),  
    }
    
    my_home_ids = zone_map.get(z, (0, 18, 19)) # Default to zone 0 if something goes wrong
    print(f"Zone is {z}. Looking for Home IDs: {my_home_ids}")
    return my_home_ids

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
    dist = horDistCalculate(robot, target)
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
    dist = horDistCalculate(robot, target)
    print(f"Distance to target: {dist}m")
    moveWithChecks(robot, dist -100, target.id)

def fullSysTest():                              #vision mvmnt + mechanism test
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = horDistCalculate(robot, target)
    mechanismOpen(servo1, servo2, robot)
    print(f"Distance to target: {dist}m")
    stepMotorsForward(robot, 2000)
    mechanismClose(servo1, servo2, robot)

angleesss = True
distssss = False
# ---MAIN LOOP--- 
print('Robot started')
indicatePowerOn(robot)

TARGET_BOXES = 3        # Number of boxes to collect before heading home - CAN EDIT MANUALLY
boxes_collected = 0

#1. Determine whether robot is looking for acids or bases
# Get our allowed IDs at the start
ALLOWED_MARKERS = decidePH() # remember to go to Vision.py to change COLLECTING_PH variable!
HOME_IDS = getHomeMarkerIds(robot)

#2. Get first acid/base marker
if COLLECTING_PH == "acid":
    getFirstAcid()
else:
    getFirstBase()

#3. -- MAIN COLLECTION LOOP (floor markers)
while boxes_colleced < TARGET_BOXES:

    targ = None
    targ_id = None
    searchStartTime = robot.time()
    print(f"Searching for {COLLECTING_PH} #{boxes_collected + 1}...")

    # STATE: SEARCHING FOR MARKER
    while targ is None:
        markers = findTargetMarker(robot) # searching for marker with closest horizontal distance
        for m in markers:
            if m.id in ALLOWED_MARKERS: # Only grabs what we are looking for
                targ = m
                targ_id = m.id
                print("Target", targ_id, "acquired")
                endSearchTime = robot.time()
                break
    #if len(markers) > 0: [just gonna comment this out...]
        # We found at least one marker!
        #targ = markers[0]
        #targ_id = targ.id
       # print(f"Target {targ.id} acquired.")
            elif notFoundMarkerTime < 3: # Little adjustment to search first:
            # No markers seen, nudge the robot and try again 
                print("Nothing seen. Nudging...")
                stepMotorsRotate(robot, 10) # Small turn - CHECK VALUES!!!!!!!
                robot.sleep(0.2)

            else: #Robot has fully lost sight of marker # -- I got up to here --
        
al = False
while not al:
    al = alignToTarget(robot, targ_id)
targ = None
markers = robot.camera.see()
for m in markers:
    if m.id == targ_id:
        targ = m
if targ:
    dist = horDistCalculate(robot, targ)
    print(f"Travelling {dist}mm now")
    stepMotorsForward(robot, convertDistToSteps(robot, dist))
    print(f"Should be at target now")
else:
    print("Lost target")
