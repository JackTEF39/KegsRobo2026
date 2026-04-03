import math
from sr.robot3 import INPUT_PULLUP, BRAKE

from Helpers import *

#Motor control:
#700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

# Motor rotation start

def stepMotorsRotateClockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = 1 #shot in the dark
    my_motor_board.motors[1].power = 1
    
    while int(robot.arduino.command("s")) - originalStep0 <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateClockwisePower(robot, steps, motorPower0, motorPower1):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = motorPower0
    my_motor_board.motors[1].power = motorPower1
    
    while int(robot.arduino.command("s")) - originalStep0 <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateAntiClockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -0.4
    my_motor_board.motors[1].power = -0.4
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps: ## check this sign pls, arent signs meant to be the same?
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateAntiClockwisePower(robot, steps, motorPower0, motorPower1):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -motorPower0
    my_motor_board.motors[1].power = -motorPower1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps: ##this one too
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

# Motor rotation end

# Motor forward/backward start

def stepMotorsForward(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = 1
    my_motor_board.motors[1].power = -1

    while (int(robot.arduino.command("s")) - originalStep0 <= steps) or (originalStep1 - int(robot.arduino.command("t")) <= steps):
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE
    my_motor_board.motors[0].power = BRAKE
    my_motor_board.motors[1].power = BRAKE

def stepMotorsForwardPower(robot, steps, motorPower0, motorPower1):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = motorPower0
    my_motor_board.motors[1].power = -motorPower1
    while (int(robot.arduino.command("s")) - originalStep0 <= steps) or (originalStep1 - int(robot.arduino.command("t")) <= steps):
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE
    my_motor_board.motors[0].power = BRAKE
    my_motor_board.motors[1].power = BRAKE

def stepMotorsBackward(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -1
    my_motor_board.motors[1].power = 1

    while (originalStep0 - int(robot.arduino.command("s"))) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE
    my_motor_board.motors[0].power = BRAKE
    my_motor_board.motors[1].power = BRAKE

def stepMotorsBackwardPower(robot, steps, motorPower0, motorPower1):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -motorPower0
    my_motor_board.motors[1].power = motorPower1

    while (originalStep0 - int(robot.arduino.command("s"))) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE
    my_motor_board.motors[0].power = BRAKE
    my_motor_board.motors[1].power = BRAKE

# Motor forward/backward start

#Individual motor stepping start
def stepMotor0AntiClockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    my_motor_board.motors[0].power = 0.4

    while int(robot.arduino.command("s")) - originalStep0 <= steps:
        pass
    my_motor_board.motors[0].power = BRAKE

def stepMotor0Clockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    my_motor_board.motors[0].power = -1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps:
        pass
    my_motor_board.motors[0].power = BRAKE

def stepMotor1AntiClockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[1].power = 1

    while int(robot.arduino.command("t")) - originalStep1 <= steps:
        pass
    my_motor_board.motors[1].power = BRAKE

def stepMotor1Clockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[1].power = 0.5

    while originalStep1 - int(robot.arduino.command("t")) <= steps:
        pass
    my_motor_board.motors[1].power = BRAKE

#Individual motor stepping end



# Motor forward/backward wrapping start - USE THESE

def stepMotors(robot, steps):
    if steps > 0:
        stepMotorsForward(robot, steps)
    elif steps < 0:
        stepMotorsBackward(robot, -steps)

def stepMotorsPower(robot, steps, motorPower0, motorPower1):
    if steps > 0:
        stepMotorsForwardPower(robot, steps, motorPower0, motorPower1)
    elif steps < 0:
        stepMotorsBackwardPower(robot, -steps, motorPower0, motorPower1)

def stepMotorsRotate(robot, steps):
    if steps > 0:
        stepMotorsRotateClockwise(robot, steps)
        #stepMotor0(robot, steps)
        #stepMotor1(robot, steps)
    elif steps < 0:
        #stepMotor0(robot, -steps)
        #stepMotor1(robot, -steps)
        stepMotorsRotateAntiClockwise(robot, -steps)

def stepMotorsRotatePower(robot, steps, motorPower0, motorPower1):
    if steps > 0:
        stepMotorsRotateClockwisePower(robot, steps, motorPower0, motorPower1)
    elif steps < 0:
        stepMotorsRotateAntiClockwisePower(robot, -steps, motorPower0, motorPower1)
# Motor forward/backward wrapping end

# Individual motor stepping start

def stepMotor0(robot, steps):
    if steps > 0:
        stepMotor0AntiClockwise(robot, steps)
    elif steps < 0:
        stepMotor0Clockwise(robot, -steps)


def stepMotor1(robot, steps):
    if steps > 0:
        stepMotor1AntiClockwise(robot, steps)
    elif steps < 0:
        stepMotor1Clockwise(robot, -steps)

# Individual motor stepping end





