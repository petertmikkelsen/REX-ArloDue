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
# 1024 x 720
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

#arlo = RobotDue.Robot()
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
arucoParams = cv2.aruco.DetectorParameters_create()
# 512 x 360
cameraMatrix = np.matrix('1766 0 512; 0 1766 360; 0 0 1')
distCoeffs = np.zeros((4,1))

def FindLandmark(robot, ids_array, maxDegreesTurned=None):
  degreesTurned = 0
  while cv2.waitKey(4) == -1: # Wait for a key pressed event
      start = time.perf_counter()
      while(True):
          if (time.perf_counter() - start > 1): # Stop after 2 second
    
            if not retval: # Error
              print(" < < <  Game over!  > > > ")
              exit(-1)
            
            if maxDegreesTurned is not None:
              if maxDegreesTurned <= degreesTurned:
                return None, None, None, degreesTurned
          
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frameReference, arucoDict, parameters=arucoParams)
            
            correct_id = None
            index_id = 0
            
            if (type(ids) is not type(None)):
              for i in range(len(ids)):
                if (ids[i] in ids_array):
                  correct_id = ids[i,0]
                  index_id = i
            
            if (type(correct_id) is not type(None)):
                rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners[index_id], 0.145, cameraMatrix, distCoeffs)
                x = tvecs[0][0,0]
                y = tvecs[0][0,1]
                dist = tvecs[0][0,2]
                v = math.acos(dist/math.sqrt(x**2 + y**2 + dist**2)) * (180 / math.pi)
                
                if (x > 0):
                   v = -v
                
                return correct_id, v, dist, degreesTurned
            else:
                robot.Turn(degrees=20, Left=False)
                degreesTurned+=20
                
            break
          else:
            retval, frameReference = cam.read() # Read frame
#ids, v, dist, degreesTurned = FindLandmark(arlo, (4, 5))
#print(ids)
#print ("id: " + str(ids));
#print ("dist: " + str(dist));
#print ("vinkel: " + str(v));
#print ("turned: " + str(degreesTurned));

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
