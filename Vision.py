from sr.robot3 import Colour, LED_A, LED_B, LED_C
import math
import cv2

from Movement import *
from Mechanism import *
CAMHEIGHT = 0.12 #height of the camera from the ground in metres
#CAMANGLE = 20 #angle of the camera to the ground in degrees


def horDistCalculate(robot, targetMarker):
    dist = targetMarker.position.distance **2 - CAMHEIGHT**2
    dist = math.sqrt(dist) / 1000
    return dist

def convertAngToSteps(robot, angle):
    steps = int(angle * STEPS_PER_DEGREE)
    return steps
    
def convertDistToSteps(robot, dist):
    steps = int(dist * STEPS_PER_MM)
    return steps


def detectId(robot):
    markers = robot.camera.see()
    for marker in markers:
        if marker.id in range(20):
            return "arena"
        elif marker.id in range(100, 140):
            return "acid"
        elif marker.id in range(140, 180):
            return "base"

def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)
            
#function to search all markers and find the target Marker (marker the shortest distance away)
def findTargetMarker(robot):
    distances = []
    markers = robot.camera.see()
    print("I can see", len(markers), "markers:")
    for marker in markers:
        if marker.id in range(100, 140): #new addition
            distances.append(marker.position.distance)
        print("Marker #{0} is {1} metres away".format(
            marker.id,
            marker.position.distance / 1000,
        ))
    targetMarkerD = min(distances)
    print("The target Marker distance is:", targetMarkerD)

    for marker in markers:
        print("The marker ID currently being tested is:", marker.id)
        print("The marker position distance currently being tested is:", marker.position.distance)
        if marker.position.distance == targetMarkerD:
            targetMarker = marker
            print("Target Marker ID is #{0}".format(
                marker.id
            ))
            return targetMarker
        else:
            print("The values do not match.")

def angCheck(robot, horA):
    if abs(horA) > 15:
        robot.kch.leds[LED_A].colour = Colour.BLUE
    elif abs(horA) < 15:
        robot.kch.leds[LED_A].colour = Colour.RED 

def distCheck(robot, dist):
    if dist > 1.5:
        robot.kch.leds[LED_A].colour = Colour.RED
        robot.kch.leds[LED_B].colour = Colour.OFF
        robot.kch.leds[LED_C].colour = Colour.OFF

    elif dist >0.3 and dist <= 1.5:
        robot.kch.leds[LED_B].colour = Colour.BLUE
        robot.kch.leds[LED_A].colour = Colour.OFF
        robot.kch.leds[LED_C].colour = Colour.OFF


    elif dist <= 0.3:
        robot.kch.leds[LED_C].colour = Colour.GREEN
        robot.kch.leds[LED_A].colour = Colour.OFF
        robot.kch.leds[LED_B].colour = Colour.OFF


    elif not dist:
        robot.kch.leds[LED_A].colour = Colour.OFF
        robot.kch.leds[LED_B].colour = Colour.OFF
        robot.kch.leds[LED_C].colour = Colour.OFF
        return 'error'


def findNextMarker360(robot):
    distances = []
    closeMarker = []
    markers = robot.camera.see()
    for i in range(12):
        if not markers:
            print("No markers detected. Rotating to search...")
            stepMotorsRotate(robot, convertAngToSteps(robot, 90))
            robot.sleep(1)
        else:
            for marker in markers:
                distances.append(marker.position.distance)
                targetMarkerD = min(distances)

            for marker in markers:
                if marker.position.distance == targetMarkerD:
                    targetMarker = marker
                    closeMarker.append(targetMarker)
                else:
                    print("The values do not match.")
            stepMotorsRotate(robot, convertAngToSteps(robot, 30))
    return min(closeMarker)


def compareTargetMarkerID(robot, targetMarkerID):
    markers = robot.camera.see()
    for marker in markers:
        print("The marker ID currently being compared is:", marker.id)
        print("The marker position distance currently being compared is:", marker.position.distance)
        if marker.id == targetMarkerID:
            targetMarker = marker
            print("Target Marker ID is #{0}".format(
                marker.id
            ))
            return targetMarker
        else:
            print("The values do not match.")

def targetMarkerAngle(targetMarker):
    horAngle = toDegrees(targetMarker.position.horizontal_angle)
    horAngle = round(horAngle,2)
    return(horAngle)

def alignToTarget(robot, target): #--FINISH LATER--
    print(f"Aligning to marker {target.id}")
    
    while True:
        markers = robot.camera.see()
        target = None
        for m in markers:
            if m.id == target.id:
                target = m
                break 
                
        if target:
            horA = targetMarkerAngle(target)
            print(f"Current angle: {horA}")
            nudge_size = convertAngToSteps(robot, horA)
            
            if abs(horA) > 2:
                stepMotorsRotate(robot, nudge_size)
            elif abs(horA) <= 2:
                print("Aligned")
                robot.kch.leds[LED_A].colour = Colour.GREEN
                robot.kch.leds[LED_B].colour = Colour.GREEN
                robot.kch.leds[LED_C].colour = Colour.GREEN
                robot.sleep(5)
                break        
        else:
            print("Lost marker, rotating")
            stepMotorsRotate(robot, convertAngToSteps(robot, 30)) # Spin to find it again
            
        robot.sleep(1)

def returnToHome(robot, my_home_ids):
    print("Action: Returning to Home")
    curr_home_id = None
    while not curr_home_id:
        markers = robot.camera.see()
        for m in markers:
            if m.id in my_home_ids:
                curr_home_id = m.id
                print(f"Home marker {curr_home_id} spotted.")
                break
        
        if curr_home_id is None:
            print("Home not in sight. Searching...")
            stepMotorsRotate(robot, 40)
            robot.sleep(1)

    alignToTarget(robot, curr_home_id)
    
    print("Aligned. Driving to zone...")
    reached = False
    while not reached:
        markers = robot.camera.see()
        for m in markers:
            if m.id == curr_home_id:
                homeM = m
                print(f"Home marker {curr_home_id} spotted.")
                break        
        if homeM:
            dist = horDistCalculate(robot, homeM)
            print(f"Distance to home: {dist}m")
            stepMotors(robot, convertDistToSteps(robot, dist))

            if dist < 150: 
                print("Inside Home Zone. Stopping.")
                reached = True
                break
        else:
            print("Lost sight of home marker. Stopping.")
            stepMotorsRotate(robot, convertAngToSteps(robot, 30)) # Spin to find it again
            robot.sleep(1)
    return

