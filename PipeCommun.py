import multiprocessing
from multiprocessing import Pipe
import time 



start = time.time()
def square_list( conn):
    """
    function to square a given list
    """
    
    i = 0 
    while True:
        now = time.time()
        delay = now-start
        print(f"\n-------putting val {i} at time:{delay} --")
        conn.send(i)
        time.sleep(4)
        i+= 1
  
def print_queue(conn):
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
  
if __name__ == "__main__":
   
    conn1,conn2 = Pipe(duplex = True)
    # creating multiprocessing Queue
    # q = multiprocessing.Queue()

    
  
    # creating new processes
    p1 = multiprocessing.Process(target=square_list, args=( [conn1]))
    p2 = multiprocessing.Process(target=print_queue, args=([conn2]))
  
    # running process p1 to square list
    
    conn1.send(88)
    time.sleep(2)
    conn2.recv()

    print('done\n')
    p1.start()
    p2.start()
   
  
    # running process p2 to get queue elements
    
    p1.join()
    p2.join()

c1, c2 = Pipe(duplex=True)
c2.send('asdf')
print(c1.recv())

# time.sleep(5)
# c2.send(c1)
# print(c1.recv())