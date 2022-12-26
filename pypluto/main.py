"Entry "
from pypluto.pluto import *
import time

if __name__ == '__main__':
    client = Drone()
    client.arm()
    time.sleep(5)
    client.steer("yaw", 100)
    client.takeoff()
    time.sleep(5)
    print("Takeoff")
    # client.getIMU()
    time.sleep(5)
    client.steer("pitch", 0)
    client.steer("yaw", 100)
    time.sleep(5)
    client.steer("yaw", 0)
    print("Disarm")
    client.disarm()
    time.sleep(5)
