from PlutoX import pluto

from subprocess import *
import time 

#necessary libraries 

# from PlutoX.Camera import poseEst

drone=pluto()
drone.connect()
drone.arm()
drone.trim(-15,-10,0,0)
drone.takeoff()
# drone.speedz(50,3)
drone.speedz(0,4)
# drone.speedy(20,4)
# drone.speedy(-40)
# drone.speedy(0)
drone.land()
drone.disarm()
time.sleep(5)


# if __name__ == "__main__":
#     poseEst.poseMain()
