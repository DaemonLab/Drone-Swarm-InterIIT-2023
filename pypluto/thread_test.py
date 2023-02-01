from pypluto import pluto
import time
#A sample program to test the drone API
drone1=pluto(DroneIP="192.168.4.1")
drone1.connect()
drone1.disarm()
drone1.arm()
time.sleep(10)
drone1.change_val()
drone1.disarm()
time.sleep(2)
drone1.arm()
time.sleep(2)
drone1.disarm()
#drone.keyboard_control()