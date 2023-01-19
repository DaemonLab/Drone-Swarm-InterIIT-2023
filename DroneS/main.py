from PlutoX import pluto
import time
drone=pluto()
drone.connect() 
drone.disarm()
#print(drone.get_vario())

drone.keyboard_control()
