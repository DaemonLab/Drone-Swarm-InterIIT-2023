# from PlutoX import pluto

# from subprocess import *
# import time 


import multiprocessing
from multiprocessing import Pipe
import time 

from PlutoX.InterFile.conn_marker_drone1 import build_conn
import PlutoX.InterFile

start = time.time()
  
if __name__ == "__main__":
   
    
    build_conn()  #starts camera file and drone1 file , also builds connection btw the two


  
    # creating new processes
    # p1 = multiprocessing.Process(target=square_list, args=( [conn1]))
    # p2 = multiprocessing.Process(target=print_queue, args=([conn2]))
  
    # running process p1 to square list
    
    # conn1.send(88)
    # time.sleep(2)
    # conn2.recv()

    # print('done\n')
    # p1.start()
    # p2.start()
   
  
    # # running process p2 to get queue elements
    
    # p1.join()
    # p2.join()

# c1, c2 = Pipe(duplex=True)
# c2.send('asdf')
# print(c1.recv())

# time.sleep(5)
# c2.send(c1)
# print(c1.recv())