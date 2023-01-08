import multiprocessing
from multiprocessing import Pipe
import time 
start = time.time()

def sender_from_marker( conn):
    """
    gives command for plan of drone1
    """
    #arm the drone here
    i = 0
    cmd = [75] # give throttle cmds 
    while True:
        now = time.time()
        delay = now-start
        print(f"\n-------putting val {i} at time:{delay} --")
        conn.send(cmd)
        time.sleep(4)
        i+= 1
  
def receiver_at_drone1(conn):
    """
    function to print queue elements
    """
    print("Queue elements:")
    
    while True :
        now = time.time()
        delay = now-start
        if (conn.poll()):
            print(f"\nListening....,{delay}, got-{conn.recv()}--now,")

        else:
            print("\nNo data available")

        # print(f"\nLength now : {q.qsize()}")
        # print()
        time.sleep(1)

    print("Queue is now empty!")