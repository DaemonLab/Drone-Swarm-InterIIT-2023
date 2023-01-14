"Entry "
from pypluto.pluto import *
import time

if __name__ == '__main__':
    client = Drone()
    client.land()
    time.sleep(5)
    client.disarm()
    #time.sleep(5)
