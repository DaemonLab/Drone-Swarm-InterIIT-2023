from PlutoX import pluto
from newPID import *
import matplotlib.pyplot as plt

drone=pluto()
camera = WebcamVideoStream(src=2).start()
# initialize PID controller
xError, yError, zError, yawError = 5, 5, 0.5, 0.3
xErrorI, yErrorI, zErrorI, yawErrorI = 0, 0, 0, 0
xErrorD, yErrorD, zErrorD, yawErrorD = 0, 0, 0, 0
xError_old, yError_old, zError_old, yawError_old = 0, 0, 0, 0

Err = [xError, yError, zError, yawError]
ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
path = []


points = [(640,360), (400,360)]

target_point = points[0]

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1, projection="3d")
drone.connect()
drone.disarm()
drone.arm()

# drone.trim(5,18,0,0) #akshit drone

drone.trim(-10,-5,0,0) #iit drone

# drone.takeoff()
# drone.speedz(0,4)
while True:
    pose, image = camera.read_pose()
    print("Aruco not detected")
    if pose is not None:
        break
drone.speedz(30,2)
# drone.speedz(0,5)
print("takeoff")


timer=0
roll_command, pitch_command, throttle_command, yawCommand = 0, 0, 0, 0
while True:
    try:
        pose, image = camera.read_pose()

        # cv2.imshow("Image", image)
        if pose is None:
            
            if timer>=500:
                print("Aruco not detected landing")
                drone.land()
                break
            timer=timer+1
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

            
            roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI = go_to(pose, [*target_point, 1.0], Err, ErrI)
            roll_command, pitch_command, throttle_command, yawCommand = int(roll_command),int(pitch_command), int(throttle_command), int(yawCommand)
            
            if np.sqrt((450-pose[0])**2+(392-pose[1])**2)<25:
                print(f"Pose: {pose}")
                print("Target Reached.")
                target_point = points[1]
                # drone.land()
                # break
                # drone.disarm()
                # break¸       
        # plt.pause(0.001) 
        drone.speedz(throttle_command)
        drone.speedx(roll_command)
        drone.speedy(pitch_command)
        drone.rotate(yawCommand)
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
