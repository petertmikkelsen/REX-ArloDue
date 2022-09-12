from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

  
# send a go_diff command to drive forward
leftSpeed = 42
rightSpeed = 46
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# Wait a bit while robot moves forward
sleep(1)

print(arlo.stop())

sleep(1)

print(arlo.go_diff(64, 70, 1, 1))
  
sleep(2.45)

print(arlo.stop())

  
print("Finished")
