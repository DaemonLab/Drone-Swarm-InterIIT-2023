from PlutoX import pluto

drone=pluto()

drone.connect()
drone.arm()


drone.trim(-10,0,0,0)
drone.takeoff()



drone.req("IMU")
  
# drone.speedz(50,3)
# drone.speedz(0)
# drone.speedy(20,3)
# drone.speedy(-40)
# drone.speedy(0)

drone.land()
drone.disarm()


