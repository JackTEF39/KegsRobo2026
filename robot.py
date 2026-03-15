from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *

robot = Robot()


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
        

def arduinoSet(pin, outState): #self explanatory.
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(pin): #self explanatory.
    return robot.arduino.pins[pin].digital_read()

def indicatePowerOn():
    robot.kch.leds[LED_A].colour = Colour.RED
    robot.kch.leds[LED_B].colour = Colour.BLUE
    robot.kch.leds[LED_C].colour = Colour.GREEN
    robot.sleep(1)
    robot.kch.leds[LED_A].colour = Colour.OFF
    robot.kch.leds[LED_B].colour = Colour.OFF
    robot.kch.leds[LED_C].colour = Colour.OFF

# Angle functions        
def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)            

def move_mm(distance):
    total_steps = int(distance * STEPS_PER_MM)
    stepMotorsForward(total_steps)

# ---MAIN LOOP--- 
print('robot started')
indicatePowerOn()

mechanismTest(servo1, servo2, robot)


targetMarker = findTargetMarker(robot)
while targetMarker is None:
    targetMarker = findTargetMarker(robot)
    if targetMarker is None:
        print("No markers found, retrying")
        robot.sleep(0.1)
    
targetMarkerId = targetMarker.id
while True:
    markers = robot.camera.see()
    found = False
    for m in markers:
        if m.id == targetMarkerId:
            targetMarker = m
            found = True
            break
    if found:
        dist = targetMarker.position.distance / 1000
        print(f"Distance to target: {dist}m")
        distCheck(dist)

    else:
        print("Target marker not found!")
        continue
    
    robot.sleep(0.1)
