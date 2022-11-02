#import cv2
import math
import numpy as np
import random
import RobotDue
import FindLandmark
from time import sleep
import copy

arlo = RobotDue.Robot()

landmarks = [1, 2, 3, 4]
landmarklocs = {2: [90, 410], 3: [510, 90], 4: [510, 410], 1: [90, 90]}

def norm(x, mu, sigma):
    return (1/(np.sqrt(2*np.pi)*sigma))*np.exp((-1/2)*(((x-mu)**2)/sigma**2))

class Particle():
    def __init__(self, x=0, y=0, theta=0, weight=0):
        self.x = x
        self.y = y
        self.theta = np.mod(theta, 360)
        self.weight = weight
    
    def initialize(self, maxX, maxY, minX=0, minY=0):
        self.x = random.random()+random.randint(minX, maxX-1)
        self.y = random.random()+random.randint(minY, maxY-1)
        self.theta = random.random()+random.randint(0, 359)
        
    
    def move(self, distance):
        distance += random.random()+(random.randint(-1, 1)*0.1*distance)
        self.x += math.sin(math.radians(self.theta))*distance*100
        self.y += math.cos(math.radians(self.theta))*distance*100

    def turn(self, degrees, right = True):
        if degrees < 0:
            right = not(right)
        degrees += (random.random()+random.randint(-5, 4))*0.0075*degrees
        self.theta = np.mod((self.theta + (int(right)*2-1)*degrees), 360)
        
    def getdist(self, x, y):
        return math.sqrt((x-self.x)**2+(y-self.y)**2)
    
    def getthetadiff(self, x, y): #given a landmarks' coordinates, returns the degrees between the particles theta and the theta if it looked towards the landmark
        vectorlandmark = [x-self.x, y-self.y]
        vectortheta = [math.sin(self.theta*math.pi/180), math.cos(self.theta*math.pi/180)]
        test = np.dot(vectortheta, vectorlandmark)
        specialdot = vectorlandmark[0]*(-vectortheta[1])+vectorlandmark[1]*vectortheta[0]
        return (180*math.acos(test/self.getdist(x, y))/math.pi) * (2*(int(specialdot<0))-1)

    def turntowardslandmark(self, thetadiff):
        if (thetadiff < 0):
            return 360+thetadiff
        else:
            return thetadiff

def estimate_pose(particles_list):
    """Estimate the pose from particles by computing the average position and orientation over all particles. 
    This is not done using the particle weights, but just the sample distribution."""
    x_sum = 0.0
    y_sum = 0.0
    cos_sum = 0.0
    sin_sum = 0.0
     
    for particle in particles_list:
        x_sum += particle.x
        y_sum += particle.y
        cos_sum += np.cos(particle.theta*math.pi/180)
        sin_sum += np.sin(particle.theta*math.pi/180)
        
    flen = len(particles_list)
    if flen != 0:
        x = x_sum / flen
        y = y_sum / flen
        theta = 180*np.arctan2(sin_sum/flen, cos_sum/flen)/math.pi
    else:
        x = x_sum
        y = y_sum
        theta = 0.0
        
    return Particle(x, y, theta)


def getweightsdist(particles, dist, thetadiff, landmarkid):
    landmark = landmarklocs[landmarkid]
    weights = np.zeros(len(particles))
    for i in range(particlenumber):
        weights[i] = max(0.000000000000001, norm(dist, particles[i].getdist(landmark[0], landmark[1]), dist*0.085))
    weights = weights/np.sum(weights)
    return getweightstheta(particles, thetadiff, landmarkid, weights)


def getweightstheta(particles, thetadiff, landmarkid, oldweights):
    weights = np.zeros(len(particles))
    landmark = landmarklocs[landmarkid]
    for i in range(particlenumber):
        weights[i] = max(0.000000000000001, norm(thetadiff, particles[i].getthetadiff(landmark[0], landmark[1]), 16))
    weights = weights*oldweights
    weights = weights/np.sum(weights)
    for i in range(len(particles)):
        particles[i].weight = weights[i]
    newparticles = np.zeros(particlenumber, dtype=Particle)
    for i in range(particlenumber):
        newparticles[i] = copy.deepcopy(np.random.choice(particles, p=weights))
    return newparticles

def updateloc(particles, targetlandmarks, maxturn = 360):
    inputlandmarks = copy.copy(targetlandmarks)
    for i in range(len(targetlandmarks)):
        ids, angle, dist, degreesturned = FindLandmark.FindLandmark(arlo, inputlandmarks, maxturn)
        for i in particles:
            i.turn(degreesturned)
        if ids is None:
            return particles
        print("found landmark id: " + str(ids))
        print("distance to landmark: " + str(dist*100+20))
        print("angle to landmark: " + str(angle))
        print("degrees turned to find landmark: " + str(degreesturned))
        particles = getweightsdist(particles, dist*100+20, -angle, ids)
        if maxturn is not None:
            maxturn -= degreesturned
            if 0 > maxturn:
                return particles
        inputlandmarks.remove(ids)
    return particles

particlenumber = 10000 #skift om nødvendigt
myparticles = np.zeros(particlenumber, dtype=Particle)
for i in range(particlenumber):
    myparticles[i] = Particle()
    myparticles[i].initialize(300, 300)
    diff = myparticles[i].getthetadiff(90,90)
    myparticles[i].theta = myparticles[i].theta + myparticles[i].turntowardslandmark(diff)
    

#indsæt opstart

for i in [[90, 90]]+list(landmarklocs.values()):
    print("going towards: " + str(i[0]) + ", " + str(i[1]))
    while (True):
        myparticles = updateloc(myparticles, landmarks)
        #potentielt brug sensor til at bestemme afstand
        bestparticle = estimate_pose(myparticles)
        if abs(bestparticle.x-i[0])<60 and abs(bestparticle.y-i[1])<60:
           print("im breaking free")
           break
        print("before driving")
        print("x: " + str(bestparticle.x))
        print("y: " + str(bestparticle.y))
        print("theta: " + str(bestparticle.theta))
        (pings, distance), turnangle = arlo.gotowards(bestparticle.x, bestparticle.y, bestparticle.theta, i[0], i[1], maxdrive=2, compensate=False)
        for j in myparticles:
            j.turn(turnangle)
            j.move(distance)
        print("turned: " + str(turnangle))
        print("drove: " + str(distance))
        bestparticle = estimate_pose(myparticles)
        print("after driving")
        print("x: " + str(bestparticle.x))
        print("y: " + str(bestparticle.y))
        print("theta: " + str(bestparticle.theta))        
        if abs(bestparticle.x-i[0])<40 and abs(bestparticle.y-i[1])<40:
            print("im breaking free")
            break
        if True in pings:
            turning = 45
            if pings[1] and not pings[2]:
                if arlo.read_sensor(3)<500:
                    turning = 15
                arlo.Turn(False, turning)
                pings, distance = arlo.Forward(0.5, compensate=True, ping=True)
                for j in myparticles:
                    j.turn(turning)
                    j.move(distance)
            elif pings[2] and not pings[1]:
                if arlo.read_sensor(2)<500:
                    turning = 15
                arlo.Turn(True, turning)
                pings, distance = arlo.Forward(0.5, compensate=True, ping=True)
                for j in myparticles:
                    j.turn(-turning)
                    j.move(distance)
            elif pings[0]:
                left = bestparticle.getthetadiff(300, 250)>0
                arlo.Turn(left, 45)
                pings, distance = arlo.Forward(0.5, compensate=True, ping=True)
                for j in myparticles:
                    j.turn(45 - 90*int(left))
                    j.move(distance)

    


arlo.Turn(degrees = 360)
arlo.Turn(True, 360)
