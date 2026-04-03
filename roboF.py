from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from MovementF import *
from VisionnF import *
from MechanismF import *
from HelpersF import *
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
    mechanismOpen(servo1, servo2, robot)
    print(f"Distance to target: {dist}m")
    stepMotorsForward(robot, 2000)
    mechanismClose(servo1, servo2, robot)

# ---MAIN LOOP--- 
                                                        ###############

# We haven't separated out the bottom and top boxes code, you sweep while trying to get floor boxes???

sweep(robot, servoTop)
mechanismClose(servo1, servo2, robot)
print("Starting...")
targ_id = findTargetMarker(robot, ).id
aligned = False

# Start - go to first marker (assumed straight on)
if targ_id != None:
    targetMarker = getMarkerFromID(robot, targ_id)
    stepMotorsForward(robot, int(targetMarker.position.distance * 0.75 * STEPS_PER_MM)) # goes 75% of the distance to the first marker

    targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for second time
    if targetMarker != None: # Once gone straight, check the marker is still in range.
        alignToTarget(robot, targ_id)

        targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for third time
        if targetMarker != None:
            mechanismOpen(robot, servo1, servo2)
            stepMotorsForward(robot, int(targetMarker.position.distance * STEPS_PER_MM)) # goes the rest of the distance to the first marker.
            mechanismClose(robot, servo1, servo2)
                                                        ############
print("Hopefully obtained first marker")

while not aligned:    
    # 1. Look for markers, align robot to marker
    markers = robot.camera.see()
    if markers:
        targ_id = findTargetMarker(robot).id
        aligned = alignToTarget(robot, targ_id)
        if aligned:
            sweeper(robot, servoTop)
            break
    else:
            print("Searching... [1 deg nudge]")
            stepMotorsRotate(robot, 20)
            robot.sleep(0.3)

# 2. GET FRESH DATA once align
robot.sleep(0.5)
markers = robot.camera.see()
final_targ = findTargetMarker(robot)

# 3. Move and Grab
if final_targ:
    dist_mm = horDistCalculate(final_targ)
    print(f"Driving {dist_mm}mm")
    
    mechanismOpen(robot, servo1, servo2) 
    
    stepMotorsForward(robot, convertDistToSteps(dist_mm))
    
    mechanismClose(robot, servo1, servo2)
    print("Grabbed!")
    
    stepMotorsForward(robot, -500)



#---STUFF THAT SIRT (wut???) IF WORKS
target = robot.camera.see()[0]
while not aligned:    
    # 1. Look for markers, align robot to marker
    markers = robot.camera.see()
    if markers:
        target = markers[0]
        last_seen_time = robot.time(robot) # Reset the timer
        print(f"Target {target.id} found! Locking on.")
        aligned = alignToTarget(robot, target_id)
    else:
        if robot.time(robot) - last_seen_time > 4.5: #Looking for marker again if robot loses sight of it for more than 2.5 seconds
            print("Searching... [1 deg nudge]")
            stepMotorsRotate(robot, 4)
            robot.sleep(0.3)


























# while distssss ==  True:
#     marks = robot.camera.see() 
    
#     if len(marks) > 0: 
#         mark = marks[0] 
#         dist = mark.position.distance / 1000
#         print(f"Marker distance: {mark.position.distance}mm") 
#         distCheck(robot, dist)
#     else:
#         print("No marker detected")
#         robot.kch.leds[LED_A].colour = Colour.OFF
#         robot.kch.leds[LED_B].colour = Colour.OFF
#         robot.kch.leds[LED_C].colour = Colour.OFF
    
#     robot.sleep(0.1) 


# while angleesss == True:
#     marks = robot.camera.see() 
    
#     if len(marks) > 0: 
#         mark = marks[0] 
#         horA = targetMarkerAngle(mark)

#         print(f"Marker angle: {horA} degrees") 
#         angCheck(robot, horA)
#     else:
#         print("No marker detected")
#         robot.kch.leds[LED_A].colour = Colour.OFF
#         robot.kch.leds[LED_B].colour = Colour.OFF
#         robot.kch.leds[LED_C].colour = Colour.OFF
    
#     robot.sleep(0.1) 
