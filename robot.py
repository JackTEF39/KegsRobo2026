#Josh fix ts smh
from sr.robot3 import Robot, OUT_H0
import math
import time
robot = Robot()
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

# Convert from radians to degrees
def toDegrees(radians):
    return radians * (180 / math.pi)

# Convert from degrees to radians
def toRadians(degrees):
    return degrees / (180 / math.pi)

# Simplified: take one marker and return its orientation values
def markerOrientation(marker):
    yaw = toDegrees(marker.position.horizontal_angle)
    pitch = marker.orientation.pitch
    roll = marker.orientation.roll
    return yaw, pitch, roll


markers = robot.camera.see()
print("I can see", len(markers), "markers:")
for marker in markers:
    print("Marker #{0} is {1} metres away".format(
        marker.id,
        marker.position.distance / 1000,
    ))

if len(markers) > 0:
    # keep `targetMarker` as the marker object (not just the id)
    minDist = None
    minRoll = None
    for marker in markers:
        print("distance",marker.position.distance)
        print("horizontal",marker.position.horizontal_angle)
        print("vertical",marker.position.vertical_angle)

    if markers[0].position.distance < markers[1].position.distance:
        targetMarker = markers[0]
    else:
        targetMarker = markers[1]
    print("Selected nearest marker id: 1 ", targetMarker.id)
    # get initial yaw from that marker
    
    yaw, pitch, roll = markerOrientation(targetMarker)
    print(f"yaw {yaw} pitch {pitch} roll {roll}")

else:
    targetMarker = None
    print("No markers visible")

# Turn until the robot's yaw reaches -90 degrees (−π/6)
if targetMarker == True:
    while yaw > -(math.pi / 6):
        count = 0
        # small step turn: include time argument
        moveRobot(0, 0.2, 0.1)
        # update markers and recompute nearest marker and its yaw
        targetMarker = robot.camera.see()
        if not targetMarker:
            print("Lost sight of markers — stopping turn")
            break 
        targetMarker = min(markers, key=lambda m: m.position.distance)
        yaw, pitch, roll = markerOrientation(targetMarker)
        count += 1
        print("Step:", count, "Current yaw:", yaw) 
        print(yaw)
        setMotors(0, 0)
        

# Turn until the robot's yaw reaches 0 degrees (0)
while yaw < 0:
    moveRobot(0, 0.5, 0.1)
        # update markers and recompute nearest marker and its yaw
    markers = robot.camera.see()
    if not markers:
        print("Lost sight of markers — stopping turn")
        break
    targetMarker = min(markers, key=lambda m: m.position.distance)
    yaw, pitch, roll = markerOrientation(targetMarker)
    