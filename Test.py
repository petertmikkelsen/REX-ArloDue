from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

lastturn = True #variable for when the robot should turn any direction (left or right)

for k in range(10):
  #arlo.Forward(compensate = True)
  print(arlo.go_diff(64, 70, 1, 1))
  pings = [] #front, back ,left, right
  for i in range(4):
    pings.append(arlo.read_sensor(i))
    sleep(0.05)
  pings = [x<1500 for x in pings]
  if pings[2] and not pings[3]:
    arlo.Turn(False)
  if pings[3] and not pings[2]:
    arlo.Turn()
  if pings[0] and pings[2] and pings[3]:
    arlo.Turn(degrees = 180)       
  if pings[0]:
    arlo.Turn(lastturn)
    lastturn = not(lastturn)
  
print("Finished")
