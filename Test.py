from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

arlo.Forward(compensate=True) #Go
  
  
print("Finished")
