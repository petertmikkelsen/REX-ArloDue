from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

print("Front sensor = ", arlo.read_front_ping_sensor())
sleep(0.041)

print(arlo.stop())
  
print("Finished")
