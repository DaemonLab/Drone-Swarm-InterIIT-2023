from PlutoX import pluto

# from subprocess import *
import time 

#necessary libraries 

# from PlutoX.Camera import poseEst

drone=pluto()
drone.connect()
drone.trim(-7,5,0,0)
# drone.arm()
# drone.speedz(0,3)
drone.takeoff()
# # drone.speedz(50,3)
drone.speedz(0,4)
# # drone.speedy(20,4)
# # drone.speedy(-40)
# # drone.speedy(0)
drone.land()
drone.disarm()


# if __name__ == "__main__":
#     poseEst.poseMain()
