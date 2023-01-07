'''Receives pose values from marker.py , computes the velocity commands for drone'''

import multiprocessing
from multiprocessing import Pipe
import time 
from PlutoX.drone import pluto

start = time.time()


def receiver_at_drone1(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    print("\nReceiving at Drone1")
    drone=pluto()
    drone.connect()
    drone.arm()
    drone.trim(-10,0,0,0)
    drone.takeoff()
    drone.speedz(50,3)
    drone.speedz(0)
    drone.speedy(20,4)
    drone.speedy(-40)
    drone.speedy(0)
    drone.land()
    drone.disarm()


    # while True :
    #     now = time.time()
    #     delay = now-start
    #     if (conn.poll()):
    #         print(f"\n{delay}--Got these cmds from pidfile: {conn.recv()}-")


    #     else:
    #         print(f"\n{delay}--No data available")

    #     # print(f"\nLength now : {q.qsize()}")
    #     # print()
    #     # time.sleep(1)

    # print("Queue is now empty!")