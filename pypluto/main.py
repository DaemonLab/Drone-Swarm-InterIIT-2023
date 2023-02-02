from pypluto import pluto
import time
#A sample program to test the drone API
# drone1=pluto(DroneIP="10.42.0.74")
drone1=pluto()
# drone2=pluto(DroneIP="10.42.0.96")
drone1.connect()
# drone2.connect()
drone1.trim(-10,10,0,0)
drone1.disarm()
# drone2.disarm()
drone1.takeoff()
drone1.throttle_speed(0,4)
drone1.land()
# drone2.arm()
# time.sleep(2)
drone1.disarm()
# drone2.disarm()
#drone.keyboard_control()