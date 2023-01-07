import multiprocessing
from multiprocessing import Pipe
import time 
from PlutoX.Control.newPIDmain import receiver_at_drone1
from PlutoX.Camera.marker import markerMainSender


#line below is for checking connectivity for testing sender , reciever functions
'''from PlutoX.InterFile.fn_of_marker_drone1 import sender_from_marker,receiver_at_drone'''
  
  
    # creating new processes
def build_conn():


    #btw marker1 file and drone1
    connCam,connDrone1 = Pipe(duplex = True)

    p1 = multiprocessing.Process(target=markerMainSender, args=( [connCam]))
    p2 = multiprocessing.Process(target=receiver_at_drone1, args=([connDrone1]))



    #first detect pose , then takeoff
    p1.start()
    print('\n------Starting process1-----')
    time.sleep(2)
    # start = time.time()
    # now= time.time()

    # while(delay<5):
    #     now = time.time()
    #     delay = now-start
    #     time.sleep(1) #enough for camera to setup
    #     print("\nSetting up camera.......")

    print("\n-----Starting process2------")
    p2.start()

    
    p1.join()
    p2.join()
   
