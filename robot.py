from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *

robot = Robot()

CAMHEIGHT = 0.12 #height of the camera from the ground in metres
#CAMANGLE = 20 #angle of the camera to the ground in degrees
DEG10 = 20 # num of degrees the robot turns for a 10 degree turn clockwise
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

def move_mm(robot, distance):
    total_steps = int(distance * STEPS_PER_MM)
    stepMotorsForward(robot, total_steps)


def visionMvnmtTest1():                          #isolated vision and mvnmt test no checks
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = distToMoveMM(robot, target)
    print(f"Distance to target: {dist}m")
    move_mm(robot, dist + 200)

def visionMvnmtTest2():                          #vision and mvnmt test with checks
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = distToMoveMM(robot, target)
    print(f"Distance to target: {dist}m")
    moveWithChecks(robot, dist + 200, target.id)

def fullSysTest():                              #vision mvmnt + mechanism test
    target = findTargetMarker(robot)
    alignToTarget(robot, target)
    dist = distToMoveMM(robot, target)
    mechanismOpen(servo1, servo2, robot)
    print(f"Distance to target: {dist}m")
    move_mm(robot, dist + 200)
    mechanismClose(servo1, servo2, robot)

angleesss = True
distssss = False
# ---MAIN LOOP--- 
print('robot started')
indicatePowerOn(robot)

# --- ALIGNMENT TEST ---
print("Searching for marker")

while True:
    markers = robot.camera.see()
    
    if len(markers) > 0:
        target = markers[0]
        print(f"Target {target.id} found. Aligning")
        alignToTarget(robot, target.id)
        
        print("Aligned! Waiting 5s")
        robot.sleep(5)
    else:
        print("No markers in sight.")
        
    robot.sleep(3)



































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
