'''Receives pose values from marker.py , computes the velocity commands for drone'''

import multiprocessing
from multiprocessing import Pipe
import time 
start = time.time()

def receiver_at_drone1(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    
    while True :
        now = time.time()
        delay = now-start
        if (conn.poll()):
            print(f"\n{delay}--Got these cmds from pidfile: {conn.recv()}-")

        else:
            print(f"\n{delay}--No data available")

        # print(f"\nLength now : {q.qsize()}")
        # print()
        time.sleep(1)

    print("Queue is now empty!")