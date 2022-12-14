# This script shows how to open a camera in OpenCV and grab frames and show these.
# Kim S. Pedersen, 2022

from math import degrees
import cv2 # Import the OpenCV library
import cv2.aruco
import numpy as np
import RobotDue
from time import sleep
import math
import time


  
  
print("Finished")

def gstreamer_pipeline(capture_width=1024, capture_height=720, framerate=30):
    """Utility function for setting parameters for the gstreamer camera pipeline"""
    return (
        "libcamerasrc !"
        "video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "videoconvert ! "
        "appsink"
        % (
            capture_width,
            capture_height,
            framerate,
        )
    )


print("OpenCV version = " + cv2.__version__)

# Open a camera device for capturing
cam = cv2.VideoCapture(gstreamer_pipeline(), apiPreference=cv2.CAP_GSTREAMER)


if not cam.isOpened(): # Error
    print("Could not open camera")
    exit(-1)

# Open a window
#WIN_RF = "Example 1"
#cv2.namedWindow(WIN_RF)
#cv2.moveWindow(WIN_RF, 100, 100)

arlo = RobotDue.Robot()
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
arucoParams = cv2.aruco.DetectorParameters_create()
cameraMatrix = np.matrix('1766 0 512; 0 1766 360; 0 0 1')
distCoeffs = np.zeros((4,1))

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    start = time.perf_counter()
    while(True):
        if (time.perf_counter() - start > 2): # Stop after 5 second
    
          if not retval: # Error
            print(" < < <  Game over!  > > > ")
            exit(-1)
          
          (corners, ids, rejected) = cv2.aruco.detectMarkers(frameReference, arucoDict, parameters=arucoParams)
        
          if (type(ids) is not type(None)):
              print('fundet kode')
              rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners, 0.145, cameraMatrix, distCoeffs)
              v = math.acos((tvecs[0][0,2])/math.sqrt((tvecs[0][0,0])**2 + (tvecs[0][0,1])**2 + (tvecs[0][0,2])**2)) * (180 / math.pi)
              print(v)
              if (tvecs[0][0,0] < 0):
                arlo.Turn(degrees = v)
              else:
                arlo.Turn(degrees = v, Left = False)
              arlo.Forward(distance = tvecs[0][0,2] - 0.2)
              
              print("done!")
              exit(-1)
          else:
              print("ikke fundet")
              arlo.Turn(degrees=30)
          break
        else:
          retval, frameReference = cam.read() # Read frame
    

    
    
    #if (type(ids) is not type(None)):
    #    print('fundet')
    #    #rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners, 0.145, cameraMatrix, distCoeffs)
    #else:
    #    print('ikke fundet')
    #    print(arlo.go_diff(46, 42, 0, 1))
    #    sleep(1)
    #    print(arlo.stop())
        
            
        
    # Show frames
    #cv2.imshow(WIN_RF, frameReference)
    

# Finished successfully
