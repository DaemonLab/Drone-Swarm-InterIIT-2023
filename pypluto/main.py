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
    client2.trim(50, -50, 0, 0)
    #client1.steer("up",400)
    # client2.steer("up",450)
    start = time.time()
    now = time.time()
    gap = now -start
    # while (gap < 5):
    #     print("a")
    #     now = time.time()
    #     gap = now - start 
    #     client2.takeoff()
    client2.takeoff()
    # client2.backFlip()
    time.sleep(4)
    #client1.land()
    client2.land()
    time.sleep(4)
    #client1.disarm()
    client2.disarm()
