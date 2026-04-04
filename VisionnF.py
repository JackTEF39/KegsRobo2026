from sr.robot3 import Colour, LED_A, LED_B, LED_C
import math
import cv2

from Movement import *
from Mechanism import *
from Helpers import *


TARGET_BOXES = 2        # Number of boxes to collect before heading home - CAN EDIT MANUALLY
boxes_collected = 0
matchStartTime = 0 
MATCH_DURATION = 150 # Total match length in seconds
ABORT_THRESHOLD = 20 # How many seconds before the end to head home

markerIDsAcquired = [] # Array to store which marker IDs robot has successfully collected
COLLECTING_PH = "acid" # MANUALLY Change this to acid or base before game starts!!


def decidePH(robot, COLLECTING_PH): 
    if COLLECTING_PH == "acid":
        # Acid markers are 100 to 139
        target_range = range(100, 140)
        print("STRATEGY: Hunting for ACIDS")
    elif COLLECTING_PH == "base":
        # Base markers are 140 to 179
        target_range = range(140, 180)
        print("STRATEGY: Hunting for BASES")
    else:
        print("This is a wall marker")
        target_range = range(0, 20)
    
    return target_range


            
#function to search all markers and find the target Marker (marker the shortest distance away)
def findTargetMarker(robot, marker_type=None, top = False):
    valid_marker = []
    markers = robot.camera.see()
    if not markers:
        stepMotors(robot, -600)
        return None
    print("I can see", len(markers), "markers:")

    for marker in markers:
        verA = targetMarkerAngleV(robot, marker)
        if not top:
            if marker.id in markerIDs[marker_type] and marker.id not in markerIDsAcquired and verA < 5: # Only grabs what we are looking for: #new addition- need to integrate zone ids
                valid_marker.append(marker)
        else:
            if marker.id in markerIDs[marker_type] and marker.id not in markerIDsAcquired and verA > 5: # Only grabs what we are looking for: #new addition- need to integrate zone ids
                valid_marker.append(marker)
    
    if valid_marker:
        targetMarker = min(valid_marker, key=lambda m: m.position.distance)
        print(f"Target Marker ID is #{targetMarker.id} at distance {targetMarker.position.distance}m")
        return targetMarker
    return None

def findNextMarker180(robot, marker_type=None):
    potentials = []
    
    stepMotorsRotate(robot, convertAngToSteps(robot, -90)) #goes 90 one way
    target = findTargetMarker(robot, marker_type)
    if target:
        potentials.append(target)
    
    stepMotorsRotate(robot, convertAngToSteps(robot, 180)) #goes 90 in other direction
    target = findTargetMarker(robot, marker_type)
    if target:
        potentials.append(target)
    
    if not potentials:
        stepMotorsRotate(robot, convertAngToSteps(robot, -90)) # return to centre
        return None
    
    best = min(potentials, key=lambda m: m.position.distance)     # picks closest

    print(f"Best marker is #{best.id} at {best.position.distance}mm")
    
    alignToTarget(robot, best.id)
    return best

def findNextMarker360(robot, marker_type=None):
    potentials = []
    
    for i in range(4): # Rotate in steps of 90 to look for markers, if 180 fails
        stepMotorsRotate(robot, convertAngToSteps(robot, 90)) #goes 90 one way
        target = findTargetMarker(robot, marker_type)
        if target:
            potentials.append(target)
    if not potentials:
        return None
    best = min(potentials, key=lambda m: m.position.distance)     # picks closest
    print(f"Best marker is #{best.id} at {best.position.distance}mm")
    
    alignToTarget(robot, best.id)
    return best



def alignToTarget(robot, target_id):
    print(f"Aligning to marker {target_id}")
    target = None
    aligned = False
    tries = 0
    while not aligned:
        target = getMarkerFromID(robot, target_id)

        if target:
            horA = targetMarkerAngleH(robot, target)
            print(f"Current angle: {horA}")
            turn_ang = convertAngToSteps(horA)
            robot.sleep(0.5)

            if abs(horA) > 5:
                stepMotorsRotate(robot, turn_ang)
                aligned = False
            elif abs(horA) <= 5:
                print("Aligned")
                aligned = True
            robot.sleep(1)
        else:
            if tries > 3:
                return aligned
            print("Lost marker, rotating")
            stepMotorsRotate(robot, convertAngToSteps(30)) # Spin to find it again
            robot.sleep(1)
            tries += 1
    return aligned

def returnToHome(robot):
    # 1. find home marker
    home = findTargetMarker(robot, "home")
    if home == None:
        home = findTargetMarker(robot, "home")
    if home == None:
        print("Cannot find home marker!")
        return False
    
    alignToTarget(robot, home.id)
    
    home = getMarkerFromID(robot, home.id)  # refresh distance
    dist = horDistCalculate(robot, home)
    stepMotors(robot, convertDistToSteps(robot, dist * 0.75))
    
    alignToTarget(robot, home.id) #realign before final approach
    
    # 5. drive the rest with checks
    home = getMarkerFromID(robot, home.id)  # refresh distance again
    dist = horDistCalculate(robot, home)
    steps_remaining = convertDistToSteps(robot, dist)
    step_size = 100  # drive in small chunks

    while steps_remaining > 0:
        stepMotors(robot, min(step_size, steps_remaining))
        steps_remaining -= step_size
        alignToTarget(robot, home.id)  # check alignment each chunk
        
        if dist < 150:
            print("Inside home zone!")
            return True
    
    return True

def obtainMarker(robot, targ_id, servo1, servo2):
    if targ_id != None:
        targetMarker = getMarkerFromID(robot, targ_id)
        stepMotorsForward(robot, int(horDistCalculate(targetMarker) * 0.75 * STEPS_PER_MM)) # goes 75% of the distance to marker

        targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for second time

        if targetMarker != None: # Once gone straight, check the marker is still in range.
            aligned = alignToTarget(robot, targ_id)

            if aligned:
                targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for third time
                if targetMarker != None:
                    mechanismOpen(robot, servo1, servo2)
                    stepMotorsForward(robot, int(horDistCalculate(targetMarker) * STEPS_PER_MM)) # goes the rest of the distance to the first marker.
                    mechanismClose(robot, servo1, servo2)
                    return True
    return False

def obtainMarkerTop(robot, targ_id, servo1, servo2, servoTop):
    if targ_id != None:
        sweep(robot, servoTop)
        targetMarker = getMarkerFromID(robot, targ_id)
        stepMotorsForward(robot, int(horDistCalculateTop(targetMarker) * 0.75 * STEPS_PER_MM)) # goes 75% of the distance to marker

        targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for second time
        if targetMarker != None: # Once gone straight, check the marker is still in range.
            alignToTarget(robot, targ_id)

            targetMarker = getMarkerFromID(robot, targ_id) # Obtain marker for third time
            if targetMarker != None:
                mechanismOpen(robot, servo1, servo2)
                stepMotorsForward(robot, int(targetMarker.position.distance * STEPS_PER_MM)) # goes the rest of the distance to the first marker.
                
                unsweep(robot, servoTop) # once it is at the marker, top mechanism goes down
                stepMotors(-1800) # go backwards to get marker on the floor
                stepMotors(900) # stab in the dark - goes forward to get the box into the robot
                mechanismClose(robot, servo1, servo2)
                return True
    return False
































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
