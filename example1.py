# This script shows how to open a camera in OpenCV and grab frames and show these.
# Kim S. Pedersen, 2022
import numpy as np
import cv2 # Import the OpenCV library
import RobotDue
from time import sleep

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

cameraMatrix = np.matrix('1766 0 512; 0 1766 360; 0 0 1')
distCoeffs = np.zeros((4,1))

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
arucoParams = cv2.aruco.DetectorParameters_create()
while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame
    
    if not retval: # Error
        print(" < < <  Game over!  > > > ")
        exit(-1)
    
    #detect ArUco kode-
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frameReference, arucoDict, parameters=arucoParams)

    if (type(ids) is not type(None)):
        print("found an id")
        rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners, 0.145, cameraMatrix, distCoeffs)
        print(tvecs[0][0,0])
        
        
        #if tvecs is less than zero then the code is to the left
        if (tvecs[0][0, 0] < 0):
          arlo.go_diff(30, 32, 0, 1) #drive left
          rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners, 0.145, cameraMatrix, distCoeffs)
          if(tvecs[0][0, 0] < -0.05): #if tvecs is close to zero then stop
            arlo.stop()
            print("1")
        elif (tvecs[0][0,0] >= 0):
          arlo.go_diff(30, 32, 1, 0)#go right
          rvecs, tvecs, markpointers= cv2.aruco.estimatePoseSingleMarkers(corners, 0.145, cameraMatrix, distCoeffs)  
          if(tvecs[0][0, 0] > 0.05): #if close to zero then stop
            arlo.stop()
            print("2")
            
            
        
#turn until tvecs
        #cv2.aruco.drawDetectedMarkers(frameReference, corners, ids)
    
        topLefty = corners[0][0,0,1]
        bottomLefty = corners[0][0,3,1]
    
        #print("TopLefty: " + str(topLefty))
        #print("BottomLefty: " + str(bottomLefty))
        #print("BottomLefty - TopLefty: " + str(bottomLefty - topLefty)) 
    #print(ids
    #else:
      #arlo.Turn(degrees = 30)
      #sleep(0.5)
    
    #image = cv2.drawFrameAxes(frameReference, cameraMatrix, distCoeffs, rvecs, tvecs, 2)
    
    #for i in ids:
    #    cv2.drawFrameAxes(frameReference, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.1)

    #objp = np.zeros(3)

    #objPoints = []
    #imgPoints = []
    #objPoints.append(objp)
    #imgPoints.append(corners)

    #cv2.calibrateCamera(objPoints, imgPoints, 1024, cameraMatrix, distCoeffs, rvecs, tvecs)

    # Show frames
    # cv2.imshow(WIN_RF, frameReference)

# Finished successfully
