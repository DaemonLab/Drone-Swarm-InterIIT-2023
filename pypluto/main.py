"Entry "
from pypluto import *
import time

if __name__ == '__main__':
    client = Drone()
    # client.arm()
    time.sleep(5)
    print("Takeoff")
    client.getIMU()
    # client.up()
    time.sleep(5)
    print("Landing")
    # client.forward()
    time.sleep(5)
    print("Disarm")
    # client.disArm()
    time.sleep(5)
