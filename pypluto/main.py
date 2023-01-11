"Entry "
from pypluto.pluto import *
import time

if __name__ == '__main__':
    #client1 = Drone("192.168.17.144","23")
    client2 = Drone("192.168.4.1","23")
    #client1.disarm()
    client2.disarm()
    time.sleep(5)
    #client1.arm()
    # time.sleep(5)
    client2.arm()
    time.sleep(5)
    #client1.steer("up",400)
    client2.steer("up",400)
    time.sleep(4)
    #client1.land()
    client2.land()
    time.sleep(4)
    #client1.disarm()
    client2.disarm()
