import numpy as np
import RobotDue
import math
import time

arlo = RobotDue.Robot()
time.sleep(0.5)
while(True):
  (pings, distance), degreesturned = arlo.Forward(compensate = True, ping = True)
  if True in pings:
    break
