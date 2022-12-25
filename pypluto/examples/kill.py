"Entry "
from pypluto import *
import time

if __name__ == '__main__':
    client = Drone()
    client.disArm()
    time.sleep(5)
