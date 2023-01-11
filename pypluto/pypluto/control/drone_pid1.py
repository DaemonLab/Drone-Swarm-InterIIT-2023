from multiprocessing import Pipe
from pypluto.pluto import Drone
import numpy as np
import time

#Target coords
xTarget,  yTarget, heightTarget = 640,360, 1.0  #pixel, pixel , height(m)

#pid gains
KPx, KPy, KPz, KPyaw = 0.06, 0.06, 500, 100
KIx, KIy, KIz, KIyaw = 0, 0, 0, 0
KDx, KDy, KDz, KDyaw = 0, 0, 0, 0


#currently global , 
#for telling drones final yaw orientation 
YAW_TARGET = 1.5708

# Radius of target threshold
THRESHOLD_R = 5



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


def pid_publisher(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    
    drone = Drone()

    # initialize PID controller
    xError, yError, zError, yawError = 5, 5, 0.5, 0.3
    xErrorI, yErrorI, zErrorI, yawErrorI = 0, 0, 0, 0
    xErrorD, yErrorD, zErrorD, yawErrorD = 0, 0, 0, 0
    xError_old, yError_old, zError_old, yawError_old = 0, 0, 0, 0

    Err = [xError, yError, zError, yawError]
    ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
    path = []
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1, projection="3d")

    drone.disarm()
    time.sleep(5)
    drone.arm()
    time.sleep(5)
    drone.steer("up",350)

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

                # if timer>=1000:
                if timeout_limit > 10 : 
                    print("Aruco not detected ,landing")
                    drone.land()
                    break

                print(f"\ntimer :{timer}")
                
          
            if pose is not None:
                start = time.time()

                print(f"Pose is {pose}")
                path.append(pose)
                timer = 0
                                                                                         
                roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI = pid(pose, [xTarget,  yTarget, heightTarget], Err, ErrI)
                
                if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<THRESHOLD_R**2:
                    print(f"Pose: {pose}")
                    print("Target Reached.")
                    
                    

            #-----------------------------
            #prev cmd if pose is none

            drone.set_steer([roll_command, pitch_command, throttle_command, yawCommand])

            '''----------------------------'''
            '''Very impt time.sleep '''
            #( if removed , it will not let you sleep)'''
            #0.03
            time.sleep(0.08)
            '''this sleep adjusts the running of this files while loop, 
            so that the rate of receiving from marker files is almost matched 
            to that of this file sending commands to drone using api '''

            '''check freq of -
            1) Frequency checker , received pose 
            2) Frequency sending '''
            '''-----------------------------'''
            #----------------------------------

            print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yawCommand}")
            # patht = np.array(path).T
            # ax.plot(patht[0], patht[1], patht[2])
            # ax.set_zlabel("Z")
            # ax.set_ylabel("Y")
            # ax.set_xlabel("X")
            

            # np.linalg.norm(np.array([xError, yError]))<10 and 
            # if np.linalg.norm(np.array([xError, yError]))<10: 
        except KeyboardInterrupt:
            break



    drone.land()
    drone.disarm()