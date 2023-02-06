from multiprocessing import Pipe
from pypluto.drone import pluto
import numpy as np
import time
import threading 





#task 3 particulars
# ------------------------------------------
#Target coords
target_array = [
    [   [375, 162],  #0
        [538, 160],  
        [652, 158],
        [788, 152],
        [882, 175] #4
    ]    
    [   
        [882, 175] 
        [920, 240], 
        [922, 332],
        [886, 402]  #
    ]
    [
        [886, 402] 
        [776, 422],
        [632, 428],
        [486, 432],
        [402, 412]#
    ]

    [ 
        [402, 412]
        [365, 355],
        [364, 248],
        [375, 162]#
    ]
]

Drone1=pluto()
Drone1.connect()

Drone2=pluto()
Drone2.connect()

Drone1ID = '0'
Drone2ID = '8'

moveDrone1 = True
moveDrone2 = False


drone1pose = None
drone2pose = None


Task_not_done = True
Rectangle1_done = False
Rectangle2_done = False 


target_idx1 = 0
target_idx2 = 4

# --------------------------------------------

# xTarget,  yTarget, heightTarget = 646, 348, 0.8 # for hover at point

# target_array2=[]
# target_array2.append(target_array[0])
# x_target,  y_target, height_target = target_array[0][0],target_array[0][1], 0.8  #pixel, pixel , height(m)







# movedict = {
#     '0' : moveDrone1,
#     '8' : moveDrone2  #id must match the drone2 ,1 selection
# }
# -----------



# ------------
#pid gains

KPx, KPy, KPz, KPyaw = 0.8, 0.4, 380 , 50
KIx, KIy, KIz, KIyaw = 0.02, 0.01, 0, 0
KDx, KDy, KDz, KDyaw = 18, 25, 10, 0


#currently global , 
#for deciding drone's final yaw orientation 
YAW_TARGET = 1.5708

def pid(pose, target, Err, ErrI):
    """
    PID Control Loop
    """
    x_error, y_error, z_error, yaw_error = Err
    x_errorI, y_errorI, z_errorI, yaw_errorI = ErrI

    x_target, y_target, height_target = target



    x_error_old = x_error
    y_error_old = y_error
    z_error_old = z_error
    yaw_error_old = yaw_error

    x,   y,   z,   yaw = pose

    x_error = x_target-x
    y_error = y_target-y
    z_error = height_target-z
    yaw_error = YAW_TARGET-yaw


    x_errorI += x_error
    y_errorI += y_error
    z_errorI += z_error
    yaw_errorI += yaw_error

    # compute derivative (variation) of errors (D)
    x_errorD = x_error-x_error_old
    y_errorD = y_error-y_error_old
    z_errorD = z_error-z_error_old
    yaw_errorD = yaw_error-yaw_error_old

    # compute commands
    xCommand = KPx*x_error + KIx*x_errorI + KDx*x_errorD
    yCommand = KPy*y_error + KIy*y_errorI + KDy*y_errorD
    zCommand = KPz*z_error + KIz*z_errorI + KDz*z_errorD

    yaw_command    = int( KPyaw*yaw_error + KIyaw*yaw_errorI + KDyaw*yaw_errorD)
    pitch_command = int( np.cos(yaw)*xCommand + np.sin(yaw)*yCommand)
    roll_command  = int( -np.sin(yaw)*xCommand + np.cos(yaw)*yCommand ) 
    throttle_command = int(zCommand)
    Err = [x_error, y_error, z_error, yaw_error]
    ErrI = [x_errorI, y_errorI, z_errorI, yaw_errorI]
    
    return roll_command, pitch_command, throttle_command, yaw_command, Err, ErrI




def move( IDX , DroneID , Err , ErrI):
     
    '''
    temp target : list of 4-5 targets,whose endpt is nxt corner 
    DroneID : '0' or '8' '''

    roll_log = []
    pitch_log = []

    
    
    #globals
    global Drone1 , Drone1ID ,drone1pose
    global Drone2, Drone2ID,  drone2pose
    global target_array 

    #Local vars
    temp_targets = target_array[IDX]
    Droneobj = None
    pose = None 
    xTarget,  yTarget, heightTarget = temp_targets[0], 348, 0.8  

    if DroneID == Drone1ID:
        Droneobj= Drone1  # ig a new instance is created ...it might not affect but is there a shorter method??
    else:
        Droneobj= Drone2


    tReachCount=0
    temp_target_idx = 0 

    while temp_target_idx != len(temp_targets)  :

        
        if DroneID == Drone1ID:
            pose = drone1pose #
        else:
            pose = drone2pose

        xTarget,  yTarget, heightTarget = temp_targets[temp_target_idx], 348, 0.8  

        try:
                
            
            if not pose : # pose is None
                
                now_time = time.time()
                timeout_limit = now_time - start 

                roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

                if timeout_limit > 8 : 
                    print("Aruco not detected ,landing")
                    Droneobj.land()
                    break
                
          
            elif (not pose)==False: #Pose not None
                
                start = time.time()
                

                #Target Vicinity counter block
                if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<25:
                    # print(f"Pose: {pose}")
                    tReachCount += 1

                    Droneobj.reset_speed()


                    #target reached corner and target is a c0.orner
                    if ( temp_target_idx == len(temp_targets)-1 and tReachCount >= 3):
                        print("\nReached Target Corner")
                        temp_target_idx +=1

                    elif (tReachCount>= 5): 
                        print("On the way Target Reached.")
                        temp_target_idx +=1
                    

                    #
                    if IDX == 3 and tReachCount >=5 : 
                        print("Task Completed\nLanding")
                        Droneobj.land()
                        time.sleep(2)
                        break


                    xTarget,  yTarget = target_array[temp_target_idx]
                    tReachCount=0

                roll_command, pitch_command, throttle_command, yaw_command, Err, ErrI = pid(pose, xTarget, yTarget, heightTarget, Err, ErrI)


                #Clipping commands
                if (roll_command>100):
                    roll_command=100
                elif (roll_command<-100):
                    roll_command=-100
                if (pitch_command>70):
                    pitch_command=70
                elif (pitch_command<-70):
                    pitch_command=-70

   
            
            # Set all speeds at once
            Droneobj.set_all_speed(roll_command, pitch_command, throttle_command, yaw_command)
            time.sleep(0.04)
       
            '''this sleep adjusts the running of this files while loop, 
            so that the rate of receiving from marker files is almost matched 
            to that of this file sending commands to drone using api '''
            
            
            if not roll_command==0:
                print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yaw_command}")

        except KeyboardInterrupt:
            break

def hover (target_coords,DroneID):

    #globals
    global moveDrone1,moveDrone2,Drone

    #locals 
    xTarget , yTarget ,heightTarget = target_coords, 0.8


    if DroneID == Drone1ID:
        Droneobj= Drone1  # ig a new instance is created ...it might not affect but is there a shorter method??
        pose = drone1pose #
    else:
        Droneobj= Drone2
        pose = drone2pose

    try:  
        
        if not pose : # pose is None
            
            now_time = time.time()
            timeout_limit = now_time - start 

            roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

            if timeout_limit > 8 : 
                print("Aruco not detected ,landing")
                Droneobj.land()

                return "Stop"
            
        
        elif (not pose)==False: #Pose not None
            
            start = time.time()
            roll_command, pitch_command, throttle_command, yaw_command, Err, ErrI = pid(pose, xTarget, yTarget, heightTarget, Err, ErrI)
            
            
            # Clipping commands
            if (roll_command>100):
                roll_command=100
            elif (roll_command<-100):
                roll_command=-100
            if (pitch_command>70):
                pitch_command=70
            elif (pitch_command<-70):
                pitch_command=-70

            # #Target Vicinity counter block
            # if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<25:
            #     # print(f"Pose: {pose}")
            #     tReachCount += 1

            #     Droneobj.reset_speed()


            #     #target reached corner and target is a c0.orner
            #     if ( temp_target_idx == len(temp_targets)-1 and tReachCount >= 3):
            #         print("\nReached Target Corner")
            #         temp_target_idx +=1

            #     elif (tReachCount>= 5): 
            #         print("On the way Target Reached.")
            #         temp_target_idx +=1
                

            #     #
            #     if IDX == 3 and tReachCount >=5 : 
            #         print("Task Completed\nLanding")
            #         Droneobj.land()
            #         time.sleep(2)
            #         return False


            #     xTarget,  yTarget = target_array[temp_target_idx]
            #     tReachCount=0

        # Set all speeds at once
        Droneobj.set_all_speed(roll_command, pitch_command, throttle_command, yaw_command)
        time.sleep(0.04)
    
        '''this sleep adjusts the running of this files while loop, 
        so that the rate of receiving from marker files is almost matched 
        to that of this file sending commands to drone using api '''
        
        
        if not roll_command==0:
            print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yaw_command}")

    except KeyboardInterrupt:
        return "stop"


    
    
    

def drone1plan():

    #global section
    global target_array, moveDrone2,moveDrone1
    global Drone1 

    #local scope
    x_error, y_error, z_error, yaw_error = 0, 0, 0, 0
    x_errorI, y_errorI, z_errorI, yaw_errorI = 0, 0, 0, 0
    x_errorD, y_errorD, z_errorD, yaw_errorD = 0, 0, 0, 0
    x_error_old, y_error_old, z_error_old, yaw_error_old = 0, 0, 0, 0

    Err = [x_error, y_error, z_error, yaw_error]
    ErrI = [x_errorI, y_errorI, z_errorI, yaw_errorI]
    path = [[0,0,0,0]]

    # Drone1=pluto()
    # # Drone1.connect()

     #Drone1.trim(-8,20,0,0) # iit
    Drone1.trim(23, 5,0,0)
    Drone1.disarm()
  
    Drone1.arm()
    Drone1.throttle_speed(300,2)
    # Drone1.takeoff()
    print("takeoff")



    tReachCount=0
    # default values when not detected
    roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

    start = time.time()
    

    target_idx1 = 0  # ranges from 0-4

    while not Rectangle1_done :
        
        if moveDrone1:  #true at very first
            rec = move(IDX= target_idx1 ,
                temp_targets= target_array[target_idx1] ,
                Droneobj= Drone1 ,
                DronePose=drone1pose,
                Err=Err,
                ErrI=ErrI  )


            #now Drone 1 has reached its temp corner pt
            moveDrone2 = True
            moveDrone1 = False 
            target_idx1 += 1

        else:

            while not moveDrone1 :
                rec = hover(target_array[target_idx1][0] )
                if (rec == "stop"):
                    break # to break plan in case of Aruco not det



def recv_pose(conn):

    '''changes the global var of poses'''

    
    global drone1pose, drone2pose


    while ( Task_not_done ):
        if (conn.poll()):                
            pose_dict = conn.recv()
            drone1pose = pose_dict[Drone1ID]
            drone2pose = pose_dict[Drone2ID]
        else: 
            drone1pose = None
            drone2pose = None





def PID_main(conn):

       

    t0 = threading.Thread( target=recv_pose , args=(conn,))
    t1 = threading.Thread( target= drone1plan, args=(10,))
    # t2 = threading.Thread( target= drone2plan, args=(10,))

    print("\nListerning to pose in 2sec")
    time.sleep(2)
    t0.start()
    time.sleep(2)
    t1.start()
    # t2.start()


    t0.join()
    t1.join()
    # t2.join()