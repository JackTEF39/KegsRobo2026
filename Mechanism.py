from sr.robot3 import Robot, Colour, OUT_L3, LED_A, LED_B, LED_C, INPUT, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

robot = Robot()

my_motor_board = robot.motor_board      #declarations
my_arduino_board = robot.arduino
my_servo_board = robot.servo_board
my_power_board = robot.power_board

servo1 = robot.servo_board.servos[0]
servo2 = robot.servo_board.servos[1]

def mechanismOpen():
    servo1.position = -0
    servo2.position = 0

def mechanismClose():
    servo1.position = 1
    servo2.position = -1   

def mechanismTest(): #currently 0 is open, 1 is closed
    mechanismOpen()
    robot.sleep(1)
    mechanismClose()
    robot.sleep(1)

def indicatePowerOn():
    robot.kch.leds[LED_A].colour = Colour.RED
    robot.kch.leds[LED_B].colour = Colour.BLUE
    robot.kch.leds[LED_C].colour = Colour.GREEN
    robot.sleep(1)
    robot.kch.leds[LED_A].colour = Colour.OFF
    robot.kch.leds[LED_B].colour = Colour.OFF
    robot.kch.leds[LED_C].colour = Colour.OFF

# ---MAIN LOOP--- 
print('robot started')
indicatePowerOn()

while True:
    mechanismTest()


