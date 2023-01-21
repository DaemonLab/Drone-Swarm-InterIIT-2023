'''This file Receives pose values from marker.py ,&
 computes the velocity commands for drone, sends them using drone.pyto='s plu'''

from multiprocessing import Pipe
from PlutoX.drone import pluto
import numpy as np
import time
# import matplotlib.pyplot as plt

#Target coords
xTarget,  yTarget, heightTarget = 640,360, 1.0  #pixel, pixel , height(m)
# 550,192
#pid gains
KPx, KPy, KPz, KPyaw = 0.225, 0.18, 200 , 70
KIx, KIy, KIz, KIyaw = 0, 0, 0, 0
KDx, KDy, KDz, KDyaw = 0, 0, 0, 0


#currently global , 
#for telling drones final yaw orientation 
YAW_TARGET = 1.5708



def pid(pose, target, Err, ErrI):
    """
    PID Control Loop
    """
    xError, yError, zError, yawError = Err
    xErrorI, yErrorI, zErrorI, yawErrorI = ErrI

    xTarget, yTarget, heightTarget = target



    xError_old = xError
    yError_old = yError
    zError_old = zError
    yawError_old = yawError

    x,   y,   z,   yaw = pose

    xError = xTarget-x
    yError = yTarget-y
    zError = heightTarget-z
    yawError = YAW_TARGET-yaw


    xErrorI += xError
    yErrorI += yError
    zErrorI += zError
    yawErrorI += yawError

    # compute derivative (variation) of errors (D)
    xErrorD = xError-xError_old
    yErrorD = yError-yError_old
    zErrorD = zError-zError_old
    yawErrorD = yawError-yawError_old

    # compute commands
    xCommand = KPx*xError + KIx*xErrorI + KDx*xErrorD
    yCommand = KPy*yError + KIy*yErrorI + KDy*yErrorD
    zCommand = KPz*zError + KIz*zErrorI + KDz*zErrorD

    yawCommand    = int( KPyaw*yawError + KIyaw*yawErrorI + KDyaw*yawErrorD)
    pitch_command = int( np.cos(yaw)*xCommand + np.sin(yaw)*yCommand)
    roll_command  = int( -np.sin(yaw)*xCommand + np.cos(yaw)*yCommand ) 
    throttle_command = int(zCommand)
    Err = [xError, yError, zError, yawError]
    ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
    
    return roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI


def receiver_at_drone1(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    
    drone=pluto()

    # initialize PID controller
    xError, yError, zError, yawError = 5, 5, 0.5, 0.3
    xErrorI, yErrorI, zErrorI, yawErrorI = 0, 0, 0, 0
    xErrorD, yErrorD, zErrorD, yawErrorD = 0, 0, 0, 0
    xError_old, yError_old, zError_old, yawError_old = 0, 0, 0, 0

    Err = [xError, yError, zError, yawError]
    ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
    path = [[0,0,0,0]]
   

    #plotting work
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1, projection="3d")
    
    drone.connect()
    drone.trim(-7,5,0,0)
    drone.disarm()
    # drone.arm()
    # drone.trim(5,18,0,0) #akshit drone

    # drone.trim(-15,-5,0,0) #iit ddrone.trim(-15,-10,0,0)rone
    # drone.trim(-5,2,0,0)

    drone.takeoff()
    # drone.throttle_speed(300,3)
    print("takeoff")

    timer=0
    roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 0, 0

    start = time.time()
    
    while True:


        try:
            pose = None
            now = time.time()
            delay = now-start

            if (conn.poll()):                
                pose = conn.recv()
                print(f"\n{delay}--Frequency checker(receiving) , received pose {pose}-")
            
            if pose is None:
                
                now_time = time.time()
                timeout_limit = now_time - start 

                roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 25, 0

                # if timer>=1000:
                if timeout_limit > 5 : 
                    print("Aruco not detected ,landing")
                    drone.land()

                print(f"\ntimer :{timeout_limit}")
                
          
            if pose is not None:
                print(f"Pose is {pose}")
                path.append(pose)
                start = time.time()
                                                                                         
                roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI = pid(pose, [xTarget,  yTarget, heightTarget], Err, ErrI)
                
                if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<25:
                    print(f"Pose: {pose}")
                    print("Target Reached.")
                    
                patht = np.array(path).T
                # ax.plot(patht[0], patht[1], patht[2])
                # ax.set_zlabel("Z")
                # ax.set_ylabel("Y")
                # ax.set_xlabel("X")
            #-----------------------------
            #prev cmd if pose is none

            drone.throttle_speed(0) #initially was 25
            drone.roll_speed(roll_command)
            drone.pitch_speed(pitch_command)
            drone.yaw_speed(yawCommand)

            '''----------------------------'''
            '''Very impt time.sleep '''
            #( if removed , it will not let you sleep)'''
            time.sleep(0.05)
            '''this sleep adjusts the running of this files while loop, 
            so that the rate of receiving from marker files is almost matched 
            to that of this file sending commands to drone using api '''

            '''check freq of -
            1) Frequency checker , received pose 
            2) Frequency sending '''
            '''-----------------------------'''
            #----------------------------------

            print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yawCommand}")
            
            # plt.pause(0.01)

            # np.linalg.norm(np.array([xError, yError]))<10 and 
            # if np.linalg.norm(np.array([xError, yError]))<10: 
        except KeyboardInterrupt:
            break



    drone.land()
    drone.disarm()
