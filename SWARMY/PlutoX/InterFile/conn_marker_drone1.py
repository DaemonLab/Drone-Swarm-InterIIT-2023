import multiprocessing
from multiprocessing import Pipe
import time 
from PlutoX.Control.drone1_pid import receiver_at_drone1
from PlutoX.Camera.marker import markerMainSender


#line below is for checking connectivity for testing sender , reciever functions
'''from PlutoX.InterFile.fn_of_marker_drone1 import sender_from_marker,receiver_at_drone'''
  
  
    # creating new processes
def build_conn():


    #btw marker1 file and drone1
    connCam,connDrone1 = Pipe(duplex = True)

    p1 = multiprocessing.Process(target=markerMainSender, args=( [connCam]))
    p2 = multiprocessing.Process(target=receiver_at_drone1, args=([connDrone1]))

    p1.start()
    time.sleep(5) #enough for camera to setup
    print("Starting process2")
    p2.start()

    
    p1.join()
    p2.join()
   
