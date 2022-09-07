from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 42
rightSpeed = 46
print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))

# Wait a bit while robot moves forward
sleep(1.1)

# send a stop command
print(arlo.stop())

print("Finished")
