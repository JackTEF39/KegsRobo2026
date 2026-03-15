from sr.robot3 import Robot, LED_A, LED_B, LED_C, Colour, OUT_H0
import math
robot = Robot()

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
            
#function to search all markers and find the target Marker (marker the shortest distance away)
def findTargetMarker():
    distances = []
    markers = robot.camera.see()
    print("I can see", len(markers), "markers:")
    for marker in markers:
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

def angCheck(horA):
    if abs(horA) > 15:
        robot.kch.leds[LED_A].colour = Colour.BLUE
    elif abs(horA) < 15:
        robot.kch.leds[LED_A].colour = Colour.RED 

def distCheck(dist):
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


    #horA = targetMarker.position.horizontal_angle
    #angCheck(horA)

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

def compareTargetMarkerID(targetMarkerID):
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

def angCheck(horA):
    if abs(horA) > 15:
        robot.kch.leds[LED_A].colour = Colour.BLUE
    elif abs(horA) < 15:
        robot.kch.leds[LED_A].colour = Colour.RED 

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

# ---MAIN LOOP--- 
targetMarker = findTargetMarker()
while targetMarker is None:
    targetMarker = findTargetMarker()
    if targetMarker is None:
        print("No markers found, retrying")
        robot.sleep(0.1)
    
targetMarkerId = targetMarker.id
while True:
    markers = robot.camera.see()
    found = False
    for m in markers:
        if m.id == targetMarkerId:
            targetMarker = m
            found = True
            break
    if found:
        dist = targetMarker.position.distance / 1000
        print(f"Distance to target: {dist}m")
        distCheck(dist)

    else:
        print("Target marker not found!")
        continue
    
    moveRobot(0.5, 0.5, 0.1)
    robot.sleep(0.1)
