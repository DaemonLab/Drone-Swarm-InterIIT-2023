from PlutoX import pluto
from PIDpose import *

drone=pluto()
position = Position(drone)
drone.connect()
drone.disarm()
drone.arm()
# drone.trim(5,15,0,0)
drone.trim(-15,-5,0,0) #iit drone


drone.takeoff()
drone.speedz(0,5)

# position.go_to([550,192])
# drone.takeoff()
# drone.speedz(50,3)
# drone.speedz(0)
# drone.speedy(20,4)
# drone.speedy(-40)
# drone.speedy(0)

drone.land()
drone.disarm()
