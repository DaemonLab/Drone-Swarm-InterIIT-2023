from PlutoX import pluto
from PIDpose import *

drone=pluto()
drone2=pluto("192.168.17.44", "23")

position = Position(drone)
drone.connect()
drone2.connect()

drone.disarm()
time.sleep(5)
drone.arm()

drone2.disarm()
time.sleep(5)
drone2.arm()
# drone.trim(5,15,0,0)

drone.trim(5,18,0,0) #akshit drone


drone.trim(-15,-5,0,0) #iit drone


# drone.takeoff()
drone.speedz(30,4)
drone2.speedz(30,4)
# drone.speedz(0,2)

# position.go_to([550,192])
# drone.takeoff()
# drone.speedz(50,3)
# drone.speedz(0)
# drone.speedy(20,4)
# drone.speedy(-40)
# drone.speedy(0)

drone.land()
drone.disarm()
drone2.land()
drone2.disarm()