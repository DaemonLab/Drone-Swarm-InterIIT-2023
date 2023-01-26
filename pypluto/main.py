from pypluto import pluto
import time
#A sample program to test the drone API
drone1=pluto(DroneIP="10.42.0.74")
drone2=pluto(DroneIP="10.42.0.96")
drone1.connect()
drone2.connect()
drone1.disarm()
drone2.disarm()
drone1.arm()
drone2.arm()
time.sleep(2)
drone1.disarm()
drone2.disarm()
#drone.keyboard_control()







