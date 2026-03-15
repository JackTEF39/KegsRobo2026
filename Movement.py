from sr.robot3 import Robot, Colour, OUT_L3, LED_A, LED_B, LED_C, INPUT, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

robot = Robot()


#How far the robot moves per step of the motor (in mm)
STEPS_PER_MM = 2.476 

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

# Motor rotation start

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

# Motor rotation end

# Motor forward/backward start

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

# Motor forward/backward start

#Individual motor stepping start
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


def returnIds():
    markers = robot.camera.see()
    for marker in markers:
        if marker.id in range(20):
            return "arena"
        elif marker.id in range(100, 140):
            return "acid"
        elif marker.id in range(140, 180):
            return "base"

# Angle functions        
def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)

def findMarkerConcise():
    distances = []
    markers = robot.camera.see()
    for marker in markers:
        distances.append(marker.position.distance)
    targetMarkerD = min(distances)

    for marker in markers:
        if marker.position.distance == targetMarkerD:
            targetMarker = marker
            return targetMarker
        else:
            print("The values do not match.")           
def alignPosition(targetId):
    print(f"Aligning to marker {targetId}")
    
    while True:
        markers = robot.camera.see()
        target = None
        for m in markers:
            if m.id == targetId:
                target = m
                break 
                
        if target:
            horA = targetMarkerAngle(target)
            print(f"Current angle: {horA}")
            nudge_size = int(abs(horA) * 5) 
            
            if horA > 2:
                stepMotorsRotate(nudge_size) # Small nudge right
            elif horA < -2:
                stepMotorsRotate(-nudge_size) # Small nudge left
            elif abs(horA) <= 2:
                print("Aligned!")
                break        
        else:
            print("Lost marker")
            stepMotorsRotate(100) # Spin to find it again
            
        robot.sleep(0.05)

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

def move_mm(distance):
    total_steps = int(distance * STEPS_PER_MM)
    stepMotorsForward(total_steps)

# ---MAIN LOOP--- 
print('robot started')
indicatePowerOn()

while True:
    stepMotorsPower(1000, 1, 1)
    mechanismTest()
