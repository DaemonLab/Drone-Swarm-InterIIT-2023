'''This file Receives pose values from marker.py ,&
 computes the velocity commands for drone, sends them using drone.pyto='s plu'''

from multiprocessing import Pipe
from pypluto.drone import pluto
import numpy as np
import time

#Target coords
target_array = [
    [914, 149],
    [921, 422],
    [365, 432],
    [375, 162],
    [914, 149]   
]
target_array2=[]
target_array2.append(target_array[0])
# xTarget,  yTarget, heightTarget = target_array[0][0],target_array[0][1], 0.8  #pixel, pixel , height(m)
xTarget,  yTarget, heightTarget = 693, 335, 0.8
Drone1=pluto(DroneIP="10.42.0.74")
# Drone2=pluto(DroneIP="10.42.0.96")
Drone1.connect()
# Drone2.connect()
# client = [Drone1,Drone2]
drone=Drone1
#pid gains
KPx, KPy, KPz, KPyaw = 0.5, 0.1, 200 , 70
KIx, KIy, KIz, KIyaw = 0.01, 0.01, 0, 0
KDx, KDy, KDz, KDyaw = 5, 30, 0, 0


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
    global xTarget,  yTarget, heightTarget, drone
    #drone=pluto()

    # initialize PID controller
    xError, yError, zError, yawError = 0, 0, 0, 0
    xErrorI, yErrorI, zErrorI, yawErrorI = 0, 0, 0, 0
    xErrorD, yErrorD, zErrorD, yawErrorD = 0, 0, 0, 0
    xError_old, yError_old, zError_old, yawError_old = 0, 0, 0, 0

    Err = [xError, yError, zError, yawError]
    ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
    path = [[0,0,0,0]]
    
    drone.trim(5, 0, 0, 0)
    Drone1.disarm()
    # Drone2.disarm()
    # drone.arm()
    # Drone1.arm()
    # Drone2.arm()
    # Drone1.throttle_speed(50,1)
    # Drone2.throttle_speed(50,1)
    Drone1.takeoff()
    # drone.throttle_speed(300,3)
    print("takeoff")

    timer=0
    roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 0, 0

    start = time.time()
    target = 0

    roll_log = []
    pitch_log = []

    while True:


        try:
            # prev_time = time.time()
            pose_dict = None
            # now = time.time()
            # delay = now-start

            if (conn.poll()):                
                pose_dict = conn.recv()
                
            
            if not pose_dict:
                
                now_time = time.time()
                timeout_limit = now_time - start 

                roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 0, 0

                if timeout_limit > 8 : 
                    print("Aruco not detected ,landing")
                    drone.land()
                    break

                # print(f"\ntimer :{timeout_limit}")
                
          
            elif (not pose_dict)==False:
                print('SGVADGV')
                print(pose_dict)
                if drone==Drone1:
                    pose=pose_dict['0']
                # elif drone==Drone2:
                #     pose=pose_dict['1']
                # path.append(pose)
                start = time.time()
                # curr_time = time.time()
                roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI = pid(pose, [xTarget,  yTarget, heightTarget], Err, ErrI)
                # print("pid calc successssssss...sending cammand")
                if (roll_command>100):
                    roll_command=100
                elif (roll_command<-100):
                    roll_command=-100
                if (pitch_command>50):
                    pitch_command=50
                elif (pitch_command<-50):
                    pitch_command=-50

                if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<100:
                    print(f"Pose: {pose}")
                    print("Target Reached.")

                    # if drone==Drone1:
                    #     target_array2.append(target_array[0])
                    #     target_array.pop(0)
                    #     drone=Drone2
                    #     if len(target_array)>1:
                    #         xTarget,  yTarget = target_array2[0]
                    #     # if not target_array:
                    #     #         drone.land()
                    # else:
                    #     target_array2.pop(0)
                    #     drone=Drone1
                    #     if not target_array2:
                    #         break
                    #     elif target_array:
                    #         xTarget,  yTarget = target_array[0]
                    #         continue

                    
                    # if target==5:
                    #     print("Task Completed\nLanding")
                    #     break
                    # xTarget,  yTarget = target_array[target]
            # if drone==Drone1:
            #     print("bheja2222222")
            #     Drone2.throttle_speed(40)
            # elif drone==Drone2:
            #     print("bheja111111")
            #     Drone1.throttle_speed(40)

            drone.throttle_speed(-5)
            # print("bhejjaaa11111")
            drone.roll_speed(roll_command)
            drone.pitch_speed(pitch_command)
            drone.yaw_speed(yawCommand)

            time.sleep(0.04)
            # prev_time = curr_time
            '''this sleep adjusts the running of this files while loop, 
            so that the rate of receiving from marker files is almost matched 
            to that of this file sending commands to drone using api '''
            if not roll_command==0:

                print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yawCommand}")

        except KeyboardInterrupt:
            break



    Drone1.land()
    Drone1.disarm()
    # Drone2.land()
    # Drone2.disarm()


