# from PlutoX.InterFile.conn_marker_drone1 import build_conn

import multiprocessing
from multiprocessing import Pipe
import time 
from pypluto.control.drone_pid1 import pid_publisher
from pypluto.ArUco.marker import pose_publisher



# builds necessary connections of drone(1,2,...) & the camera file
def build_conn():


    #creates connection btw marker1 file and drone1
    connCam,connDrone1 = Pipe(duplex = True)



    p1 = multiprocessing.Process(target=pose_publisher, args=( [connCam]))
    p2 = multiprocessing.Process(target=pid_publisher, args=([connDrone1]))


    
    #first detect pose , then takeoff
    p1.start()
    print('\n-------Starting process Camera-------')
    time.sleep(2)

    # while(delay<5):
    #     now = time.time()
    #     delay = now-start
    #     time.sleep(1) #enough for camera to setup
    #     print("\nSetting up camera.......")

    print("\n-----Starting Drone1--------")
    p2.start()
    
    p1.join()
    p2.join()
   


  
if __name__ == "__main__":
   
    
    build_conn() 
