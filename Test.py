from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

# arlo.Forward(compensate=True, distance=2) #Go
# print("Finished")
for i in range(5):
  print(i + ":" + arlo.read_front_ping_sensor())
