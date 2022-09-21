from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

# arlo.Forward(compensate=True, distance=2) #Go
# print("Finished")

print(arlo.read_front_ping_sensor())
