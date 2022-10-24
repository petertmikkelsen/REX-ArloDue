import numpy as np
import RobotDue
import math
import time

arlo = RobotDue.Robot()
time.sleep(0.5)
while(True):
  arlo.Forward(compensate = True, ping = True)
