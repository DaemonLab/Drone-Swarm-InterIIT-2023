"Entry "
from pypluto.pluto import *
#import time

if __name__ == '__main__':
    #client1 = Drone("192.168.17.144","23")
    client2 = Drone("192.168.4.1","23")
    #client1.disarm()
    client2.disarm()
    time.sleep(5)
    #client1.arm()
    # time.sleep(5)
    client2.arm()
    client2.trim(-10, -25, 0, 0)   #Ak Drone  15, 15, 40, 0
    time.sleep(5)
    #client2.steer("up",400)
    client2.steer("up",450)
    # client2.backFlip()
    time.sleep(5)
    #client1.land()
    client2.land()
    time.sleep(4)
    #client1.disarm()
    client2.disarm()
