from sr.robot3 import Colour, LED_A, LED_B, LED_C

from Movement import *

def mechanismOpen(robot, servo1, servo2):
    servo1.position = -0
    servo2.position = 0

def mechanismClose(robot, servo1, servo2):
    servo1.position = 1
    servo2.position = -1   

def mechanismTest(robot, servo1, servo2): #currently 0 is open, 1 is closed
    mechanismOpen(robot, servo1, servo2)
    robot.sleep(1)
    mechanismClose(robot, servo1, servo2)
    robot.sleep(1)

def indicatePowerOn(robot):
    robot.kch.leds[LED_A].colour = Colour.RED
    robot.kch.leds[LED_B].colour = Colour.BLUE
    robot.kch.leds[LED_C].colour = Colour.GREEN
    robot.sleep(3)
    robot.kch.leds[LED_A].colour = Colour.OFF
    robot.kch.leds[LED_B].colour = Colour.OFF
    robot.kch.leds[LED_C].colour = Colour.OFF

def sweep(robot, servo):
    servo.position = 1
    robot.sleep(0.5)
    stepMotorsRotate(robot, 90)
    servo.position = 0
    robot.sleep(0.5)

def unsweep(robot, servo):
    servo.position = 0
    robot.sleep(0.5)
    servo.position = 1
    robot.sleep(0.5)

def deposit(robot, servo1, servo2):
    print("Depositing")
    mechanismOpen(robot, servo1, servo2)
    robot.sleep(1)
    stepMotors(robot, stepMotors(robot, 200)) # Move back to deposit 
    mechanismClose(robot, servo1, servo2)
    stepMotorsRotate(robot,60)

def sweeper(robot, servo1, servo2):
    print("Sweeping")
    stepMotors(robot, stepMotors(robot, 200)) # Move forward to sweep
    sweep(robot, servo1)
    robot.sleep(1)
    stepMotors(robot, convertDistToSteps(robot, -200)) # Move back after sweeping
