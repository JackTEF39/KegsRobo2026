import cv2
from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT, INPUT_PULLUP, OUTPUT, BRAKE, Note

robot = Robot()

#Motor control:
#700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

my_motor_board = robot.motor_board      #declarations
my_arduino_board = robot.arduino
my_servo_board = robot.servo_board
my_power_board = robot.power_board

robot.servo_board.servos[7].position = 0
my_motor_board.motors[0].power = 0

robot.arduino.pins[3].mode = INPUT_PULLUP
robot.arduino.pins[2].mode = INPUT_PULLUP
robot.arduino.pins[5].mode = INPUT_PULLUP
robot.arduino.pins[4].mode = INPUT_PULLUP
        
usefulServo1 = my_servo_board.servos[0]

def arduinoSet(pin, outState): 
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(pin):
    return robot.arduino.pins[pin].digital_read()

#def arduinoSetTime(pin, outState, time):
    #arduinoSet(pin, outState)
    #robot.sleep(time)

#def squareFreq(pin, freq):
    #arduinoSetTime(pin, True, (1 / freq) / 2)
    #print(robot.arduino.pins[2].digital_read())
    #arduinoSetTime(pin, False, (1 / freq) / 2)
    #print(robot.arduino.pins[2].digital_read())

#def squareTime(pin, onTime, offTime):
    #arduinoSetTime(3, True, onTime)
    #arduinoSetTime(3, False, offTime)

def stepMotorsRotateClockwise(steps):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = 1
    my_motor_board.motors[1].power = 1
    
    while int(robot.arduino.command("s")) - originalStep0 <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateClockwisePower(steps, motorPower0, motorPower1):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = motorPower0
    my_motor_board.motors[1].power = motorPower1
    
    while int(robot.arduino.command("s")) - originalStep0 <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateAntiClockwise(steps):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -1
    my_motor_board.motors[1].power = -1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsRotateAntiClockwisePower(steps, motorPower0, motorPower1):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -motorPower0
    my_motor_board.motors[1].power = -motorPower1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsForward(steps):
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

def stepMotorsForwardPower(steps, motorPower0, motorPower1):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = motorPower0
    my_motor_board.motors[1].power = -motorPower1

    while int(robot.arduino.command("s")) - originalStep0 <= steps or originalStep1 - int(robot.arduino.command("t")) <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsBackward(steps):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -1
    my_motor_board.motors[1].power = 1

    while originalStep0 - int(robot.arduino.command("s")) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsBackwardPower(steps, motorPower0, motorPower1):
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -motorPower0
    my_motor_board.motors[1].power = motorPower1

    while originalStep0 - int(robot.arduino.command("s")) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsPower(steps, motorPower0, motorPower1):
    if steps > 0:
        stepMotorsForward(steps, motorPower0, motorPower1)
    elif steps < 0:
        stepMotorsBackward(-steps, motorPower0, motorPower1)

def stepMotor0AntiClockwise(steps):
    originalStep0 = int(robot.arduino.command("s"))
    my_motor_board.motors[0].power = 1

    while int(robot.arduino.command("s")) - originalStep0 <= steps:
        pass
    my_motor_board.motors[0].power = BRAKE

def stepMotor0Clockwise(steps):
    originalStep0 = int(robot.arduino.command("s"))
    my_motor_board.motors[0].power = -1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps:
        pass
    my_motor_board.motors[0].power = BRAKE

def stepMotor1AntiClockwise(steps):
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[1].power = 1

    while int(robot.arduino.command("t")) - originalStep1 <= steps:
        pass
    my_motor_board.motors[1].power = BRAKE


def stepMotor1Clockwise(steps):
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[1].power = 1

    while originalStep1 - int(robot.arduino.command("t")) <= steps:
        pass
    my_motor_board.motors[1].power = BRAKE

def stepMotors(steps):
    if steps > 0:
        stepMotorsForward(steps)
    elif steps < 0:
        stepMotorsBackward(-steps)

def stepMotorsPower(steps, motorPower0, motorPower1):
    if steps > 0:
        stepMotorsForwardPower(steps, motorPower0, motorPower1)
    elif steps < 0:
        stepMotorsBackwardPower(-steps, motorPower0, motorPower1)

def stepMotorsRotate(steps):
    if steps > 0:
        stepMotorsRotateClockwise(steps)
    elif steps < 0:
        stepMotorsRotateAntiClockwise(-steps)

def stepMotorsRotatePower(steps, motorPower0, motorPower1):
    if steps > 0:
        stepMotorsRotateClockwisePower(steps, motorPower0, motorPower1)
    elif steps < 0:
        stepMotorsRotateAntiClockwisePower(-steps, motorPower0, motorPower1)


def stepMotor0(steps):
    if steps > 0:
        stepMotor0AntiClockwise(steps)
    elif steps < 0:
        stepMotor0Clockwise(-steps)


def stepMotor1(steps):
    if steps > 0:
        stepMotor1AntiClockwise(steps)
    elif steps < 0:
        stepMotor1Clockwise(-steps)
        

    
stepMotors(9000)


