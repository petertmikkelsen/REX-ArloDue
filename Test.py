import numpy as np
import RobotDue
import math
import time

arlo = RobotDue.Robot()
time.sleep(1)
arlo.Forward(3, ping=True)
