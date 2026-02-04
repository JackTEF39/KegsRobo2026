import math, time
import cv2
from sr.robot3 import Robot, Colour, LED_A, OUT_H0


robot = Robot(wait_for_start=False)
my_motor_board = robot.motor_board
my_arduino_board = robot.arduino
my_servo_board = robot.servo_board

def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)

def markerOrientationYaw():
    markers = robot.camera.see()
    for marker in markers:
        yaw = marker.position.horizontal_angle
        yawD = toDegrees(marker.position.horizontal_angle)
        return yaw, yawD

def moveRobot(leftPower, rightPower, time): #sets motors and holds for (time) seconds
    robot.motor_board.motors[0].power = leftPower
    robot.motor_board.motors[1].power = rightPower
    robot.sleep(time)
    robot.motor_board.motors[0].power = 0
    robot.motor_board.motors[1].power = 0
    return


def colcheck():
    markers = robot.camera.see()
    for marker in markers:
        distance = marker.position.distance

    if distance > 1.5:
        robot.kch.leds[LED_A].colour = Colour.RED
    elif distance >0.3 and distance <= 1.5:
        robot.kch.leds[LED_A].colour = Colour.BLUE
    elif distance <= 0.3:
        robot.kch.leds[LED_A].colour = Colour.GREEN
    elif not distance:
        return 'error'
    return distance

robot.servo_board.servos[7].position = 0

if 1 < 2: 
    print(markerOrientationYaw())


while True
    if colcheck() > 0.1:
        for i in range(0, 1500, 100):
            markerOrientation()
            moveRobot(0.1, 0.1, 1)
            print(colcheck() / 1000)
            robot.sleep(0.2)
    elif colcheck() == 'error
        or_fix()
else:
    break


def or_fix():
    markers = robot.camera.see()
    for marker in markers:
        print(marker.orientation.yaw)
        if yaw != 0:
            if marker.orientation.yaw > 0:
                moveRobot(0.0, -0.5, 0.1)
            elif marker.orientation.yaw < 0:
                moveRobot(0.0, 0.5, 0.1)
    return
