

from PlutoX.drone import pluto
import time

if __name__ == '__main__':
    client =pluto()
    client.disarm()
    time.sleep(5)
