from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

print(arlo.go_diff(64, 69, 1, 1))

sleep(2.3)

print(arlo.stop())

sleep(1)

# send a go_diff command to drive forward
leftSpeed = 42
rightSpeed = 46
print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))

# Wait a bit while robot moves forward
sleep(2.44)

# send a stop command
print(arlo.stop())

sleep(1)

print(arlo.go_diff(64, 69, 1, 1))

sleep(2.3)

print(arlo.stop())

sleep(1)

# send a go_diff command to drive forward
leftSpeed = 42
rightSpeed = 46
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# Wait a bit while robot moves forward
sleep(2.2)

print(arlo.stop())

print("Finished")
