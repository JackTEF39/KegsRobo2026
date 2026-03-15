from sr.robot3 import INPUT_PULLUP, BRAKE

#How far the robot moves per step of the motor (in mm)
STEPS_PER_MM = 2.476 

#Motor control:
#700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

def arduinoSet(robot, pin, outState): #self explanatory.
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(robot, pin): #self explanatory.
    return robot.arduino.pins[pin].digital_read()

# Motor rotation start

def stepMotorsRotateClockwise(robot ,steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = 1
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
    my_motor_board.motors[0].power = -1
    my_motor_board.motors[1].power = -1
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps:
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
    
    while originalStep0 - int(robot.arduino.command("s")) <= steps or originalStep1 - int(robot.arduino.command("t")) >= steps:
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

    while int(robot.arduino.command("s")) - originalStep0 <= steps or originalStep1 - int(robot.arduino.command("t")) <= steps:
        if int(robot.arduino.command("s")) - originalStep0 >= steps:
            my_motor_board.motors[0].power = BRAKE
        if originalStep1 - int(robot.arduino.command("t")) >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsBackward(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -1
    my_motor_board.motors[1].power = 1

    while originalStep0 - int(robot.arduino.command("s")) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

def stepMotorsBackwardPower(robot, steps, motorPower0, motorPower1):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    originalStep1 = int(robot.arduino.command("t"))
    my_motor_board.motors[0].power = -motorPower0
    my_motor_board.motors[1].power = motorPower1

    while originalStep0 - int(robot.arduino.command("s")) <= steps or int(robot.arduino.command("t")) - originalStep1 <= steps:
        if originalStep0 - int(robot.arduino.command("s")) >= steps:
            my_motor_board.motors[0].power = BRAKE
        if int(robot.arduino.command("t")) - originalStep1 >= steps:
            my_motor_board.motors[1].power = BRAKE

# Motor forward/backward start

#Individual motor stepping start
def stepMotor0AntiClockwise(robot, steps):
    my_motor_board = robot.motor_board
    originalStep0 = int(robot.arduino.command("s"))
    my_motor_board.motors[0].power = 1

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
    my_motor_board.motors[1].power = 1

    while originalStep1 - int(robot.arduino.command("t")) <= steps:
        pass
    my_motor_board.motors[1].power = BRAKE

#Individual motor stepping end

# Motor forward/backward wrapping start - USE THESE

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
# Motor forward/backward wrapping end

# Individual motor stepping start

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

# Individual motor stepping end

def move_mm(distance):
    total_steps = int(distance * STEPS_PER_MM)
    stepMotorsForward(total_steps)


