# Arlo Robot Controller

from time import sleep
import time
import serial
import math
import numpy as np


class Robot(object):
    """Defines the Arlo robot API
    
       DISCLAIMER: This code does not contain error checking - it is the responsibility
       of the caller to ensure proper parameters and not to send commands to the 
       Arduino too frequently (give it time to process the command by adding a short sleep wait
       statement). Failure to do some may lead to strange robot behaviour.
       
       In case you experience trouble - consider using only commands that do not use the wheel 
       encoders.
    """ 
    def __init__(self, port = '/dev/ttyACM0'):
        """The constructor port parameter can be changed from default value if you want
           to control the robot directly from your labtop (instead of from the on-board raspberry 
           pi). The value of port should point to the USB port on which the robot Arduino is connected."""
        self.port = port
        
        #self.serialRead = serial.Serial(self.port,9600, timeout=1) # 1 sec. timeout, wait until data is received or until timeout
        self.serialRead = serial.Serial(self.port,9600, timeout=None) # No timeout, wait forever or until data is received

        # Wait if serial port is not open yet
        while not self.serialRead.isOpen():
            sleep(1)

        print("Waiting for serial port connection ...")
        sleep(2)

        print("Running ...")
        
    def __del__(self):
        print("Shutting down the robot ...")
        
        sleep(0.05)
        print(self.stop())
        sleep(0.1)
                
        cmd='k\n'
        print((self.send_command(cmd)))
        self.serialRead.close()
        
        
    def send_command(self, cmd, sleep_ms=0.0):
        """Sends a command to the Arduino robot controller"""
        self.serialRead.write(cmd.encode('ascii'))
        sleep(sleep_ms)
        str_val=self.serialRead.readline()
        return str_val


    def _power_checker(self, power):
        """Checks if a power value is in the set {0, [30;127]}.
           This is an internal utility function."""
        return  (power == 0) or (power >=30 and power <=127) 

        
    def go_diff(self, powerLeft, powerRight, dirLeft, dirRight):
        """Start left motor with motor power powerLeft (in {0, [30;127]} and the numbers must be integer) and direction dirLeft (0=reverse, 1=forward)
           and right motor with motor power powerRight (in {0, [30;127]} and the numbers must be integer) and direction dirRight (0=reverse, 1=forward).
        
           The Arlo robot may blow a fuse if you run the motors at less than 40 in motor power, therefore choose either 
           power = 0 or 30 < power <= 127.
           
           This does NOT use wheel encoders."""
        
        if (not self._power_checker(powerLeft)) or (not self._power_checker(powerRight)):
            print("WARNING: Read the docstring of Robot.go_diff()!")
            return ""
        else:
            cmd = 'd' + str(int(powerLeft)) + ',' + str(int(powerRight)) + ',' + str(int(dirLeft)) + ',' + str(int(dirRight)) + '\n'
            return self.send_command(cmd)


    def stop(self):
        """Send a stop command to stop motors. Sets the motor power on both wheels to zero.
        
           This does NOT use wheel encoders."""
        cmd='s\n'
        return self.send_command(cmd)


    
    def read_sensor(self, sensorid):
        """Send a read sensor command with sensorid and return sensor value. 
           Will return -1, if error occurs."""
        cmd=str(sensorid) + '\n'
        str_val=self.send_command(cmd)
        if len(str_val) > 0:
            return int(str_val)
        else:
            return -1
            
    def read_front_ping_sensor(self):
        """Read the front sonar ping sensor and return the measured range in milimeters [mm]"""
        return self.read_sensor(0)
        
    def read_back_ping_sensor(self):
        """Read the back sonar ping sensor and return the measured range in milimeters [mm]"""
        return self.read_sensor(1)
        
    def read_left_ping_sensor(self):
        """Read the left sonar ping sensor and return the measured range in milimeters [mm]"""
        return self.read_sensor(2)
        
    def read_right_ping_sensor(self):
        """Read the right sonar ping sensor and return the measured range in milimeters [mm]"""
        return self.read_sensor(3)

    
    def read_left_wheel_encoder(self):
        """Reads the left wheel encoder counts since last reset_encoder_counts command.
           The encoder has 144 counts for one complete wheel revolution."""
        cmd='e0\n'
        return self.send_command(cmd, 0.045)

    def read_right_wheel_encoder(self):
        """Reads the right wheel encoder counts since last clear reset_encoder_counts command.
           The encoder has 144 counts for one complete wheel revolution."""
        cmd='e1\n'
        return self.send_command(cmd, 0.045)

    def reset_encoder_counts(self):
        """Reset the wheel encoder counts."""
        cmd='c\n'
        return self.send_command(cmd)
    

    ### MOVEMENT FOR ARLO DUE

    def Forward(self, distance = 1, powerLeft = 64, powerRight = 70, compensate = False, ping = False):
        """drives forward. unless otherwise specified, will drive 1 meter, with compensation designed for ArloDue"""  
        if compensate: #for some reason this might not work
            self.go_diff(42, 46, 0, 1)
            sleep(0.15)
            self.stop()
            sleep(0.1) #wait .1 second before next command
        if distance > 0:  
            driving = False
            start = time.perf_counter()
            while(True):
                if (time.perf_counter()-start<distance*2.45):
                    if ping:
                        pings = []
                        for i in [0, 2, 3]:
                            pings.append(self.read_sensor(i)<200*(1+int(i==0)))
                            sleep(0.03)
                        if True in pings:
                            self.stop()
                            return pings, (time.perf_counter()-start)/2.45
                    if not (driving):
                        driving = True
                        self.go_diff(powerLeft, powerRight, 1, 1)
                        sleep(0.03)
                else:
                    self.stop()
                    return [False, False, False], distance
    
    def Turn(self, Left=True, degrees=90, speed=1, compensate = False):
        """Turns to the side, if 'Left' variable is set to True, it will turn left, otherwise it will turn right"""
        #note that speed variable is experimental and not reliable, it should be set to 1 preferably
        if degrees <= 0 or speed <= 0:
            return
        sleeptime = 1 #sleeptime is the time it takes to turn 90 degrees assuming speed=1
        if Left and not compensate:
            sleeptime = 1.22
        if Left and compensate:
            #not found, this is only an estimation:
            sleeptime = 1.3
        if not Left and not compensate:
            sleeptime = 1.1
        if not Left and compensate:
            sleeptime = 1
        self.go_diff(46*speed, 42*speed, int(not Left), int(Left))
        sleep(((degrees/90)*sleeptime)/speed)
        self.stop()
        
    def gotowards(self, x, y, theta, targetx, targety, maxdrive=1, compensate = True):
        vectortarget = [targetx-x, targety-y]
        vectortheta = [math.sin(theta*math.pi/180), math.cos(theta*math.pi/180)]
        test = np.dot(vectortheta, vectortarget)
        specialdot = vectortarget[0]*(-vectortheta[1])+vectortarget[1]*vectortheta[0]
        distance = math.sqrt((targetx-x)**2+(targety-y)**2)
        turnangle = (180*math.acos(test/distance)/math.pi) * (2*(int(specialdot<0))-1)
        if turnangle>0:
            self.Turn(False, turnangle, compensate=compensate)
            returning = turnangle
        elif turnangle<0:
            self.Turn(degrees = -turnangle, compensate=compensate)
            returning = turnangle
        sleep(0.2)
        return self.Forward(min(distance/100, maxdrive), ping=True), returning
        
    def Circle(self, Left, stop = True):
        """drive in a circle, ending up at the original point. if variable 'left' is true, the circle will turn left"""
        if Left:
            # send a go_diff command to drive forward
            leftSpeed = 0
            rightSpeed = 45
            print(self.go_diff(0, 45, 1, 1))
            sleep(10.5)
            if stop:
                self.stop()
        if not Left:
            print(self.go_diff(90, 45, 1, 1))
            sleep(6.2)
            if stop:
                self.stop()

    def Reverse(self, distance = 1, powerLeft = 64, powerRight = 70):
        """drives forward. unless otherwise specified, will drive 1 meter, with compensation designed for ArloDue"""  
        if distance > 0:  
            self.go_diff(powerLeft, powerRight, 0, 0)
            sleep(distance*2.45)
            self.stop()             
                
                                
    def pings(self):
        return [self.read_sensor(0), self.read_sensor(1), self.read_sensor(2), self.read_sensor(3)] #front, back, left, right

    ### OBSOLETE STUFF
        
    def go(self):
        """OBSOLETE: Send a go command for continuous forward driving using the wheel encoders"""
        cmd='g\n'
        return self.send_command(cmd)
        
    def backward(self):
        """OBSOLETE: Send a backward command for continuous reverse driving using the wheel encoders"""
        cmd='v\n'
        return self.send_command(cmd)
        

    def left(self):
        """OBSOLETE: Send a rotate left command for continuous rotating left using the wheel encoders"""
        cmd='n\n'
        return self.send_command(cmd)

    def right(self):
        """OBSOLETE: Send a rotate right command for continuous rotating right using the wheel encoders"""
        cmd='m\n'
        return self.send_command(cmd)
        
    def step_forward(self):
        """OBSOLETE: Send a step forward command for driving forward using the wheel encoders for a 
           predefined amount of time"""
        cmd='f\n'
        return self.send_command(cmd)

    def step_backward(self):
        """OBSOLETE: Send a step backward command for driving backward using the wheel encoders for a 
           predefined amount of time"""
        cmd='b\n'
        return self.send_command(cmd)

    def step_rotate_left(self):
        """OBSOLETE: Send a step rotate left command for rotating left using the wheel encoders for a 
           predefined amount of time"""
        cmd='l\n'
        return self.send_command(cmd)
        
    def step_rotate_right(self):
        """OBSOLETE: Send a step rotate right command for rotating right using the wheel encoders for 
           a predefined amount of time"""
        cmd='r\n'
        return self.send_command(cmd)
            
        
    def set_speed(self, speed):
        """OBSOLETE: Speed must be a value in the range [0; 255]. This speed is used in commands based on 
           using the wheel encoders."""
        cmd='z' + str(speed) + '\n'
        return self.send_command(cmd)
        
    def set_turnspeed(self, speed):
        """OBSOLETE: Turnspeed must be a value in the range [0; 255]. This speed is used in commands based on 
           using the wheel encoders."""
        cmd='x' + str(speed) + '\n'
        return self.send_command(cmd)

    def set_step_time(self, steptime):
        """OBSOLETE: steptime is the amount of miliseconds used in the step_forward and step_backwards 
           commands."""
        cmd='t' + str(steptime) + '\n'
        return self.send_command(cmd)
        
    def set_turn_time(self, turntime):
        """OBSOLETE: turntime is the amount of miliseconds used in the step_rotate_left and 
        step_rotate_right commands."""
        cmd='y' + str(turntime) + '\n'
        return self.send_command(cmd) #this is a test wawaaw, oasjd
        
