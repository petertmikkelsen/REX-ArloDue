from time import sleep

import RobotDue

# Create a robot object and initialize
arlo = RobotDue.Robot()

print("Running ...")

print("Front sensor = ", arlo.read_front_ping_sensor())
sleep(0.041)

# request to read Back sonar ping sensor
print("Back sensor = ", arlo.read_back_ping_sensor())
sleep(0.041)

# request to read Right sonar ping sensor
print("Right sensor = ", arlo.read_right_ping_sensor())
sleep(0.041)

# request to read Left sonar ping sensor
print("Left sensor = ", arlo.read_left_ping_sensor())
sleep(0.041)

print(arlo.stop())
  
print("Finished")
