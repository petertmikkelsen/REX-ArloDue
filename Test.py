from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

lastturn = True #variable for when the robot should turn any direction (left or right)
  
while(True):
  #arlo.Forward(compensate = True)
  pings = [] #front, back ,left, right
  for i in range(4):
    pings.append(arlo.read_sensor(i))
    sleep(0.05)
  print(pings)
  pings = [x<1500 for x in pings]
  if pings[2] and not pings[3]:
    arlo.Turn(False)
  elif pings[3] and not pings[2]:
    arlo.Turn()
  elif pings[0] and pings[2] and pings[3]:
    arlo.Turn(degrees = 180)       
  elif pings[0]:
    arlo.Turn(lastturn)
    lastturn = not(lastturn)
  else:
    print(arlo.go_diff(64, 70, 1, 1))
    sleep(2.45)
    print(arlo.stop())
    sleep(0.1)
  
  
print("Finished")
