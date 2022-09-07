from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = 55
rightSpeed = 90
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

sleep(6)

if (False):
  # send a go_diff command to drive forward
  leftSpeed = 90
  rightSpeed = 45
  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

  sleep(6)

print(arlo.stop())
  
print("Finished")
