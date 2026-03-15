from sr.robot3 import Colour, LED_A, LED_B, LED_C

def mechanismOpen(servo1, servo2, robot):
    servo1.position = -0
    servo2.position = 0

def mechanismClose(servo1, servo2):
    servo1.position = 1
    servo2.position = -1   

def mechanismTest(servo1, servo2, robot): #currently 0 is open, 1 is closed
    mechanismOpen(servo1, servo2, robot)
    robot.sleep(1)
    mechanismClose(servo1, servo2, robot)
    robot.sleep(1)

def indicatePowerOn(robot):
    robot.kch.leds[LED_A].colour = Colour.RED
    robot.kch.leds[LED_B].colour = Colour.BLUE
    robot.kch.leds[LED_C].colour = Colour.GREEN
    robot.sleep(1)
    robot.kch.leds[LED_A].colour = Colour.OFF
    robot.kch.leds[LED_B].colour = Colour.OFF
    robot.kch.leds[LED_C].colour = Colour.OFF
