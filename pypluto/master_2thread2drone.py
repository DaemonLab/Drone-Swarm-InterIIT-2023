import matplotlib

import time 
from pypluto.Control.task3_toge import PID_main
from pypluto.Camera.marker import marker_publisher

from pypluto.pypluto.Control.task3_toge_2thread2drone import MissionPlanner
from pypluto.pypluto.Control.task3_toge_2thread2drone import CameraTask3


import threading
import cv2


 


# builds necessary connections of drone(1,2,...) & the camera file
def build_conn():

    global pose1,pose2

    CT = CameraTask3()

    #creates connection bt  w marker1 file and drone1
    # connCam,connDrone1 = Pipe(duplex = True)

    

    # MP = MissionPlanner() #use CT only

    f1 = threading.Thread(target= CT.dronePlan , args=('0')) 
    f2 = threading.Thread(target= CT.dronePlan , args=('8')) 

    start = time.time()

    cap  = cv2.VideoCapture(0)
    counter = 0
    while(True):
        counter += 1 #make sure counter is checked for 1 
        ret , img = cap.read()

        now= time.time()
        tim = now -start 

        #start threads when req.
        if (tim > 20 and counter ==1):
            f1.start()
            f2.start()

        CT.POSEDICT  = marker_publisher(img)

    p1 = multiprocessing.Process(target=marker_publisher, args=( [connCam]))
    p2 = multiprocessing.Process(target=PID_main, args=([connDrone1]))



    #first detect pose , then takeoff
    p1.start()
    print('\n-------Starting process Camera-------')
    time.sleep(2)

    print("\n-----Starting Drone1--------")
    p2.start()

    
    p1.join()
    p2.join()
    

  
if __name__ == "__main__":
   

    
    
    build_conn()  #starts camera file and drone1 file , also builds connection btw the two

