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

