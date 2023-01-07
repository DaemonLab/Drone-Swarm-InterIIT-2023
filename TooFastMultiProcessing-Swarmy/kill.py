

from PlutoX import Drone
import time

if __name__ == '__main__':
    client = Drone()
    client.disarm()
    time.sleep(5)
