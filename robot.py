from sr.robot3 import Robot, OUT_H0
import math

#Making 1 motor 50% power and the other 0% power for 1 second makes the robot turn 90 degrees.
#arena boundary is range(20)
#acidic samples are range(100, 140)
#basic samples are range(140, 180)
#for now I'll just get acids

def moveRobot(leftPower, rightPower, time): #sets motors and holds for (time) seconds
    robot.motor_board.motors[0].power = leftPower
    robot.motor_board.motors[1].power = rightPower
    robot.sleep(time)
    robot.motor_board.motors[0].power = 0
    robot.motor_board.motors[1].power = 0
    return

def setMotors(leftPower, rightPower): #just sets motors
    robot.motor_board.motors[0].power = leftPower
    robot.motor_board.motors[1].power = rightPower

def moveUntilFrontBelow(distance):
    distance_front = robot.arduino.ultrasound_measure(2, 3)

    while distance_front > distance:
        distance_front = robot.arduino.ultrasound_measure(2, 3)
        print(distance_front)

def printIds():
    markers = robot.camera.see()
    for marker in markers:
        if marker.id in range(20):
            print("arena")
        elif marker.id in range(100, 140):
            print("acid")
        elif marker.id in range(140, 180):
            print("base")

def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)
            
robot = Robot()
powerBoard = robot.power_board
moveRobot(0.8, 0.5, 1)
markers = []
currentMarker = None
while True:
    setMotors(0, 0)
    moveRobot(0.5, 0, 1)
    markers = robot.camera.see() 

    for marker in markers: #sees until an acid is found.

        if marker.id in range(100, 140): #and marker.position.vertical_angle < 0.2: #if the marker is an acid and not raised it goes towards it.
            currentMarker = marker
            moveRobot(0.5 * (toDegrees(marker.position.horizontal_angle) / 90), 0, 1) #turn to face the acid then go toward it.

            while robot.arduino.ultrasound_measure(2, 3) > 50:
                moveRobot(0.8, 0.5, 0.4)
            powerBoard.outputs[OUT_H0].is_enabled = True #turn vacuum on

            #at this point vision is useless so we need to go by colour to get back to our lab.
            
            while True: #turn back to the lab
                moveRobot(0.5, 0, 1)
                markers = robot.camera.see()
                for marker in markers:
                    if marker.id == labID:
                        moveRobot(0.5 * (toDegrees(marker.position.horizontal_angle) / 90), 0, 1)
                        #use reflectance sensors to find our way back to the base
