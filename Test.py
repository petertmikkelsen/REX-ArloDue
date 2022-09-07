from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")
for i in range(4):
  print(arlo.go_diff(42, 46, 1, 1))
  
  sleep(3.45)

  print(arlo.stop())
  break
  sleep(1) #wait before new command

  # send a go_diff command to drive forward
  leftSpeed = 42
  rightSpeed = 46
  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

  # Wait a bit while robot moves forward
  sleep(1.1)

  # send a stop command
  print(arlo.stop())
  
  sleep(1) #wait before new command

print("Finished")
