# from PlutoX import pluto
from PlutoX.Control.newPID import *
# import matplotlib.pyplot as plt
# from PlutoX.Camera.ignore_poseEst import WebcamVideoStream


'''Receives pose values from marker.py , computes the velocity commands for drone'''
import multiprocessing
from multiprocessing import Pipe
import time 
from PlutoX.drone import pluto


start = time.time()


def receiver_at_drone1(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    print("\nReceiving at Drone1")

    
    drone=pluto()
    print('here1')
    # camera = WebcamVideoStream(src=2)
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
    drone.connect()
    drone.disarm()
    drone.arm()
    print('here2')
    # drone.trim(5,18,0,0) #akshit drone

    drone.trim(-15,-5,0,0) #iit drone
    estart = time.time()
    print('here')
    # drone.takeoff()
    while True:
        print("inside while ")
        # time.sleep(2)
        # pose, image = camera.read_pose()
        pose = None

        now = time.time()
        delay = now-estart

        if (conn.poll()):
            print(f"\n{delay}--Got these cmds from pidfile: {conn.recv()}-")
            pose = conn.recv()

        else:
            # print(f"\n{delay}--No data available")
            print("Aruco not detected")
            pass
        
        if pose is not None:
            break

    print('ahead of while')
    drone.speedz(30,2)
    # drone.speedz(0,5)
    print("takeoff")

    timer=0
    roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 0, 0

    
    while True:

        start = time.time()
        now_time = time.time()

        try:
            # pose, image = camera.read_pose()

            pose = None
            now = time.time()
            delay = now-start

            if (conn.poll()):
                pose = conn.recv()
                print(f"\n{delay}--Got these cmds from pidfile: {pose}-")

            else:
                # print(f"\n{delay}--No data available")
                pass

            # cv2.imshow("Image", image)

            
            if pose is None:
                
                now_time = time.time()
                timeout_limit = now_time - start 

                # if timer>=1000:
                if timeout_limit > 5: 
                    print("Aruco not detected ,landing")
                    drone.land()
                # timer=timer+1
                print(f"\ntimer :{timer}")
                # if timeout == 0:
                #     start = time.time()
                #     timeout = 1
                #     print('TIMEOUT START')
                # if timeout == 1 and (time.time()-start == 5):
                #     print("Aruco not detected landing")
                #     drone.land()


                

                
                
            if pose is not None:
                path.append(pose)
                timer = 0

                
                roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI = go_to(pose, [640,360, 1.0], Err, ErrI)
                roll_command, pitch_command, throttle_command, yawCommand = int(roll_command),int(pitch_command), int(throttle_command), int(yawCommand)
                
                if np.sqrt((450-pose[0])**2+(392-pose[1])**2)<25:
                    print(f"Pose: {pose}")
                    print("Target Reached.")
                    # drone.land()
                    # break
                    # drone.disarm()
                    # break¸       
            # plt.pause(0.001) 

            #-----------------------------
            # drone.speedz(throttle_command)
            # drone.speedx(roll_command)
            # drone.speedy(pitch_command)
            # drone.rotate(yawCommand)
            #----------------------------------

            print(f"rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yawCommand}")
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