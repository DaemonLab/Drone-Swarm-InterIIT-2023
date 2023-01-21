from PlutoX import pluto
import time
drone=pluto()
drone.connect() 
drone.disarm()
drone.trim(-2,2,0,0)
drone.takeoff()

drone.throttle_speed(0,3)
drone.land()
drone.disarm()
# drone.keyboard_control()
