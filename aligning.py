





def targetMarkerAngle(targetMarker):
    horAngle = toDegrees(targetMarker.position.horizontal_angle)
    horAngle = round(horAngle,2)
    return(horAngle)

def alignToMarker(targetId):
    print(f"Aligning to marker {targetId}...")
    
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

            if abs(horA) <= 2:
                setMotors(BRAKE, BRAKE)
                print("Aligned!")
                break
            
            if horA > 0:
                stepMotorsRotate(nudge_size) # Small nudge right
            else:
                stepMotorsRotate(-nudge_size) # Small nudge left
        else:
            print("Target lost during alignment! Searching...")
            stepMotorsRotate(100) # Spin to find it again
            
        robot.sleep(0.05)