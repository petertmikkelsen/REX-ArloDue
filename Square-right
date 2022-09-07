from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

print(arlo.go_diff(42, 46, 0, 1))

# Wait a bit while robot moves forward
sleep(0.2)

# send a stop command
print(arlo.stop())

sleep(1) #wait before new command

for i in range(4):
  
  print(arlo.go_diff(64, 70, 1, 1))
  
  sleep(2.45)

  print(arlo.stop())
  
  sleep(1) #wait before new command
  
  # send a go_diff command to drive forward
  leftSpeed = 42
  rightSpeed = 46
  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

  # Wait a bit while robot moves forward
  sleep(0.9)

  # send a stop command
  print(arlo.stop())
  
  sleep(1) #wait before new command

print(arlo.go_diff(42, 46, 1, 0))

# Wait a bit while robot moves forward
sleep(0.1)

# send a stop command
print(arlo.stop())
  
print("Finished")
