
from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note

import math

import robot

STEPS_PER_MM = 2.476  #How far robot moves per step (in mm)
STEPS_PER_DEGREE = 4.4 #number of steps for 1° turn (guess)
CAMHEIGHT = 120 #height of camera from the ground in mm

def getHomeMarkerIds(robot):
    z = robot.zone 
    zone_map = {
        0: (0, 18, 19),    
        1: (3, 4, 5),    
        2: (8, 9, 10), 
        3: (13, 14, 15),  
    }
    
    my_home_ids = zone_map.get(z, (0, 18, 19)) # Default to zone 0 if something goes wrong
    print(f"Zone is {z}. Looking for Home IDs: {my_home_ids}")
    return my_home_ids

markerIDs = {
    "acid": range(100, 140),
    "base": range(140, 180),
    "arena": range(0, 20),
}

def getMarkerType(marker_id):  
    for type_name, id_range in markerIDs.items():
        if marker_id in id_range:
            return type_name
    return None

def getMarkerFromID(robot, target_id):
    markers = robot.camera.see()
    for marker in markers:
        if marker.id == target_id:
            return marker
    return None


def arduinoSet(robot, pin, outState): #self explanatory.
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(robot, pin): #self explanatory.
    return robot.arduino.pins[pin].digital_read()

def toDegrees(radians):
    return radians * (180 / math.pi)

def toRadians(degrees):
    return degrees / (180 / math.pi)

def horDistCalculate(targetMarker):
    dist = targetMarker.position.distance **2 - CAMHEIGHT**2
    dist = math.sqrt(dist)
    return dist

def convertAngToSteps(angle):
    steps = int(angle * STEPS_PER_DEGREE)
    return steps
    
def convertDistToSteps(dist):
    steps = int(dist * STEPS_PER_MM)
    return steps

def targetMarkerAngleH(targetMarker):
    horAngle = toDegrees(targetMarker.position.horizontal_angle)
    horAngle = round(horAngle,2)
    return horAngle

def targetMarkerAngleV(targetMarker):
    verAngle = toDegrees(targetMarker.position.vertical_angle)
    verAngle = round(verAngle,2)
    return verAngle


def indicatePowerOn(robot):
    robot.kch.leds[LED_A].colour = Colour.RED
    robot.kch.leds[LED_B].colour = Colour.BLUE
    robot.kch.leds[LED_C].colour = Colour.GREEN
    robot.sleep(3)
    robot.kch.leds[LED_A].colour = Colour.OFF
    robot.kch.leds[LED_B].colour = Colour.OFF
    robot.kch.leds[LED_C].colour = Colour.OFF

