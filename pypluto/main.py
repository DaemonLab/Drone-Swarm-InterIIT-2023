"Entry "
from pypluto.pluto import *
import time

if __name__ == '__main__':
    client = Drone()
    client.arm()
    time.sleep(5)
    print("Takeoff")
    # client.getIMU()
    client.move("X", 200)
    time.sleep(5)
    client.move("X", 0)
    client.move("Y", 100)
    time.sleep(5)
    client.move("Y", 0)
    print("Disarm")
    client.disarm()
    time.sleep(5)
