
import threading
import time 
import pypluto.Control.task3_toge  as Task3




#for camera part
import cv2

CAMERA_HEIGHT = 1.9 

Aruco_ref_dist = 2.2 # may be same as camera ht if we use it as a reference
Aruco_ht_pixels_grnd =15 #ht in pixels when aruco on ground( reference dist)
Aruco_width_pixels_grnd = 15 #wdth in pixels when aruco on ground( reference dist)
Aruco_len_pixels_grnd = 15

#matrix_coefficients - Intrinsic matrix of the calibrated camera
MATRIX_COEFFICIENTS = np.array([[
            1447.9804004365824,
            0.0,
            617.3063266183908
        ],
        [
            0.0,
            1448.4116664252433,
            289.02239681156016
        ],
        [
            0.0,
            0.0,
            1.0
        ]])

#distortion_coefficients - Distortion coefficients associated with our camera
DISTORTION_COEFFICIENTS = np.array([
            0.0397515407032859,
            1.259291585298002,
            -0.010631456171277863,
            -0.00784841820297665,
            -5.925444820936321
        ])
    
class Aruco:

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.                    DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    def __init__(self, arucoType):
        self.arucoType = arucoType
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[self.arucoType])
        self.arucoParams = cv2.aruco.DetectorParameters_create()

    def detectMarkers(self,img):
        
        return cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)

    def get_pose(self, corners, ids, image, desiredVec, display=True):

        is_detected = False
        pose = None

        
        if len(corners) > 0:
            
            for (markerCorner, markerID) in zip(corners, ids):


                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(np.array(corners), 0.02, cameraMatrix=MATRIX_COEFFICIENTS, distCoeffs=DISTORTION_COEFFICIENTS)

                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = np.array([int(topRight[0]), int(topRight[1])])
                bottomRight = np.array([int(bottomRight[0]), int(bottomRight[1])])
                bottomLeft = np.array([int(bottomLeft[0]), int(bottomLeft[1])])
                topLeft = np.array([int(topLeft[0]), int(topLeft[1])])

                #-----------------------------------for drone ht calc

                deltax1 = topRight[0]- bottomRight[0]
                deltay1 = topRight[1]- bottomRight[1]
                len1 = np.sqrt( np.power(deltax1,2) + np.power(deltay1,2)  )
                dist_l1 = Aruco_ref_dist*(1-(Aruco_len_pixels_grnd/ len1))
                dist_l1 = round(dist_l1 , 3)

                deltax2 = topLeft[0]- bottomLeft[0]
                deltay2 = topLeft[1]- bottomLeft[1]
                len2 = np.sqrt( np.power(deltax2,2) + np.power(deltay2,2)  )
                dist_l2 = Aruco_ref_dist*(1-(Aruco_len_pixels_grnd/ len2))
                dist_l2 = round(dist_l2 , 3)


                deltax3 = topRight[0]- topLeft[0]
                deltay3 = topRight[1]- topLeft[1]
                width1 = np.sqrt( np.power(deltax3,2) + np.power(deltay3,2)  )
                dist_w1 = Aruco_ref_dist*(1-(Aruco_width_pixels_grnd/ width1))
                dist_w1 = round(dist_w1 , 3)

                deltax4 = bottomRight[0]- bottomLeft[0]
                deltay4 = bottomRight[1]- bottomLeft[1]
                width2 = np.sqrt( np.power(deltax4,2) + np.power(deltay4,2)  )
                dist_w2 = Aruco_ref_dist*(1-(Aruco_width_pixels_grnd/ width2))
                dist_w2 = round(dist_w2 , 3)


                distmax = round( max( max(dist_l1 , dist_l2 ) , max( dist_w1 , dist_w2) ) ,3  )

                if distmax < 0 :
                    distmax = 0 
                #------------------------------------
                
 
                cX, cY = (topLeft + bottomRight)//2
                hX, hY = (topLeft + topRight)//2
                tX, tY = hX-cX, hY-cY
                yaw = np.arctan2(tY, tX) 


                    
                drone_height = CAMERA_HEIGHT - tvec[0,0,2]

                pose = np.array([cX,cY, drone_height,yaw]) 
                is_detected = True
                if display:
                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                    

                    cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                    
                    cv2.arrowedLine(image, (cX,cY), (hX,hY),(0, 0, 255))

                    cv2.putText(image , f"distmax:{distmax}  ",
                    (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
        if display:
            for i in range(len(desiredVec[0])):

                dX,dY = desiredVec[0][i]
                cv2.circle(image, (dX, dY), 7, (255, 0, 0), -1)

            cv2.imshow("Image", image)        

                
        return pose, is_detected, image, 




#extras 
#for toge_task3 part
from pypluto.drone import pluto
import numpy as np


YAW_TARGET = 1.5708

# --------
#pid gains

KPx, KPy, KPz, KPyaw = 0.8, 0.4, 380 , 50
KIx, KIy, KIz, KIyaw = 0.02, 0.01, 0, 0
KDx, KDy, KDz, KDyaw = 18, 25, 10, 0


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



class MissionPlanner():
   

    def __init__(self) :
        #Target coords


        #For Recieving Pose
        # self.conn = conn 


        self.target_array = [
            [   [375, 162],  #0
                [538, 160],  
                [652, 158],
                [788, 152],
                [882, 175] #4
            ],    
            [   
                [882, 175],
                [920, 240], 
                [922, 332],
                [886, 402]  #
            ],
            [
                [886, 402],
                [776, 422],
                [632, 428],
                [486, 432],
                [402, 412]#
            ],
            [ 
                [402, 412],
                [365, 355],
                [364, 248],
                [375, 162]#
            ]
        ]
        self.Drone1=pluto(DroneIP='10.42.0.61')
        self.Drone1.connect()
        self.Drone1.disarm()

        self.Drone2=pluto(DroneIP='10.42.0.74')
        self.Drone2.connect()
        self.Drone2.disarm()

    
        self.compliDict = {
            '0' : '8',
            '8' : '0'
        }
        self.START_OUTER_IDX = {
            '0' : 0,
            '8' : 3 # as this corresponds to 2 subarray, and is given to IDX
        }
        self.DRONEOBJDICT = {
            '0' : self.Drone1 ,
            '8' : self.Drone2
        }
        self.Drone1ID = '8'
        self.Drone2ID = '0'


        self.moveDrone1 = True
        self.moveDrone2 = False

        self.MOVEDICT = {
            '0' : self.moveDrone1,
            '8' : self.moveDrone2,
        }

        self.poseDrone1 = None
        self.poseDrone2 = None

        self.POSEDICT = {
            '0' : self.poseDrone1,
            '8' : self.poseDrone2
        }


        self.Task_not_done = True
        self.Rectangle1_done = False
        self.Rectangle2_done = False 

        self.RECT_DONE_DICT = {
            '0' : self.Rectangle1_done ,
            '8' : self.Rectangle2_done     
        }

        self.target_idx1 = 0
        self.target_idx2 = 4

        self.TARGET_IDX_DICT = {
            '0' : self.target_idx1 ,
            '1' : self.target_idx2 
        }

        #currently global , 
        #for deciding drone's final yaw orientation 
        self.YAW_TARGET = 1.5708  # we can change the yaw for each here YAW_TARGET1 & YAW_TARGET2
         
    
        
    def move( self, IDX , DroneID , Err , ErrI):
        
        '''
        temp target : list of 4-5 targets,whose endpt is nxt corner 
        DroneID : '0' or '8' '''

        roll_log = []
        pitch_log = []


        #Local vars
        temp_targets = self.target_array[IDX]
        Droneobj = self.DRONEOBJDICT[DroneID]
        pose = self.POSEDICT[DroneID]


        #locals
        xTarget,  yTarget, heightTarget = temp_targets[0][0] , temp_targets[0][1], 0.8  


        #
        tReachCount=0
        temp_target_idx = 0 

        start = time.time()
        while temp_target_idx != len(temp_targets)  : #loop till idx just greater than last ele


            #to change target within temp array ( one corner to other)
            xTarget,  yTarget, heightTarget = temp_targets[0][0] , temp_targets[0][1], 0.8  


            pose = self.POSEDICT[DroneID]
            

            try:
                    
                if not pose : # pose is None
                    
                    now_time = time.time()
                    time_detected = now_time - start 

                    roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

                    if time_detected> 8 : 
                        print(f"\nAruco not detected ,landing : {DroneID}\n")
                        Droneobj.land()
                        return 'not det'
                        
                    
                elif (not pose)==False: #Pose not None
                    

                    start = time.time()
                    
                    #Target Vicinity counter block
                    if np.sqrt((xTarget-pose[0])**2+(yTarget-pose[1])**2)<25:
                        # print(f"Pose: {pose}")
                        tReachCount += 1

                        Droneobj.reset_speed() #why??? to avoid overshooting after targets


                        # corner target reached  , then idx+1   
                        if ( IDX < (self.START_OUTER_IDX[DroneID]-1)%4  and temp_target_idx == len(temp_targets)-1 and tReachCount >= 5):
                            print(f"\nReached Target Corner {temp_target_idx}, ;{DroneID}\n")
                            temp_target_idx +=1
                            break 

                        #On the way targets reached , then idx+1 and reset tReachCounter
                        elif (temp_target_idx < len(temp_targets)-1 and tReachCount>= 5 ): 
                            print(f"\nOn the way Target Reached. : {DroneID} , Target : {IDX,temp_target_idx}\n")
                            temp_target_idx +=1
                            tReachCount=0


                        #Last target in last array , just land & break
                        if IDX == (self.START_OUTER_IDX[DroneID]-1)%4 and temp_target_idx == len(temp_targets)-1 and tReachCount >=10 : 
                            print(f"\nTask Completed\nLanding , {DroneID}")
                            Droneobj.land()
                            time.sleep(2)
                            return "stop"
                            

                    
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
                
                
                # if not roll_command==0:
                print(f"\n(sending) move , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yaw_command}")

            except KeyboardInterrupt:
                Droneobj.disarm()
                print(f"Disarming Drone {DroneID}")
                time.time(2)
                return 'interupt'
 
    def hover (self, target_coords,DroneID):


        #locals 
        xTarget , yTarget ,heightTarget = target_coords[0], target_coords[1], 0.8
        Droneobj = self.DRONEOBJDICT[DroneID]
        pose = self.POSEDICT[DroneID]   
        move_state =  self.MOVEDICT[DroneID]
        start = time.time()
        while (not move_state):

            pose = self.POSEDICT[DroneID]   
            move_state =  self.MOVEDICT[DroneID]

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
                    
                    print(f"\nHovering {DroneID} at {xTarget,yTarget}")
                    # Clipping commands
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
                
                
                # if roll_command !=0:
                print(f"\nHover :  rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yaw_command}")

            except KeyboardInterrupt:
                Droneobj.disarm()
                print(f"Disarming Drone {DroneID}")

                return "interupt"

    def dronePlan(self,DroneID):


        print(f"\n-----Starting Drone {DroneID} plan--------")
        
        

        #local scope
        x_error, y_error, z_error, yaw_error = 0, 0, 0, 0
        x_errorI, y_errorI, z_errorI, yaw_errorI = 0, 0, 0, 0
        x_errorD, y_errorD, z_errorD, yaw_errorD = 0, 0, 0, 0
        x_error_old, y_error_old, z_error_old, yaw_error_old = 0, 0, 0, 0

        Err = [x_error, y_error, z_error, yaw_error]
        ErrI = [x_errorI, y_errorI, z_errorI, yaw_errorI]
        path = [[0,0,0,0]]



        DroneObj= self.DRONEOBJDICT[DroneID]
        move_state = self.MOVEDICT[DroneID]
        # # Drone1.connect()

        #Drone1.trim(-8,20,0,0) # iit
        DroneObj.trim(23, 5,0,0)#  ??????????????
        DroneObj.disarm()
        DroneObj.arm()

        DroneObj.throttle_speed(300,3)
        # DroneObj.takeoff()
        print(f"Takeoff: {DroneID}")


        # default values when not detected
        roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

        start = time.time()
        
        Rectangle_done = self.RECT_DONE_DICT[DroneID]
        IDX = self.START_OUTER_IDX[DroneID] # goes from 0 to 4
    
        '''need to tell when drone ids rect is done'''
        while not Rectangle_done :
            
            move_state = self.MOVEDICT[DroneID]
            

            if move_state :  #true at very first for drone1 and False for drone2
                resp = self.move(IDX= IDX, DroneID=DroneID,Err=Err,ErrI=ErrI  )
                #now current Drone  has reached its temp corner pt , so make itself hover and other move
                self.MOVEDICT[DroneID] = False
                self.MOVEDICT[self.compliDict[DroneID]] = True

                #change current drones outer idx to nxt, (and pass 1st element of this new sub array to hover)
                
                #last 
                if( IDX == (self.START_OUTER_IDX[DroneID]-1) %4 ):
                    Rectangle_done  = True
                    DroneObj.land()
                    print(f"Rectangle{DroneID} Done")
                    time.sleep(2)

                #shift to next set of temp array

                if(resp == 'stop' or 'not det'): 
                    print(f"\n\nresp (move): {resp}")
                    break #reached final 15th target

            else:                                               #last element of subarray
                resp = self.hover( self.target_array[IDX][ len(self.target_array[IDX])-1 ] , DroneID=DroneID)

                #nxt IDX to get nxt subarray to move (above in nxt loop) 
                IDX += 1 
                
                self.MOVEDICT[DroneID] = True
                self.MOVEDICT[self.compliDict[DroneID]] = False


                if (resp == "stop" or "not det" or 'interupt'):
                    print(f"\nresp (hover) : {resp}")
                    break # to break plan in case of Aruco not det
            
            Rectangle_done = self.RECT_DONE_DICT[DroneID]
   
    def marker_publisher(self):  #connCam

        print('\n-------Starting process Camera-------')
        time.sleep(2)

        cameraID = 2 # your camera id on pc
        target_array = [
        [375, 162],
        [538, 160],
        [652, 158],
        [788, 152],
        [914, 149],
        [920, 240],
        [922, 332],
        [921, 422],
        [776, 422],
        [632, 428],
        [486, 432],
        [365, 432],
        [365, 355],
        [364, 248],
        [375, 162],
        ]

        cap = cv2.VideoCapture(cameraID)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        aruco_obj = Aruco("DICT_4X4_50")

        while cap.isOpened(): 

            ret, image = cap.read()               
            
            #Aruco Detection , pose Estimation Block

            pose_dict={}
            corners, ids, rejected = aruco_obj.detectMarkers(image)
            # print(ids)

            

            if len(corners)>0:
                for i in range(0,len(ids)):
                    pose, is_detected, detected_markers  = aruco_obj.get_pose(corners[i], ids, image, [target_array], display=True)
                    cv2.imshow("Image", detected_markers)
                    pose_dict[str(ids[i][0])]=pose

                    

            else:
                for i in range(len(target_array)):

                    dX,dY = target_array[i]
                    cv2.circle(image, (dX, dY), 7, (255, 0, 0), -1)

                cv2.imshow("Image", image)
            
            # print(pose_dict)
            # connCam.send(pose_dict)
            self.POSEDICT = pose_dict 


            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()


# builds necessary connections of drone(1,2,...) & the camera file
def build_conn():


    MP = Task3.MissionPlanner()

    T0  = threading.Thread(target = MP.marker_publisher)
    # t0 = threading.Thread( target= MP.recv_pose )
    t1 = threading.Thread( target= MP.dronePlan, args=(MP.Drone1ID))
    t2 = threading.Thread( target= MP.dronePlan, args=(MP.Drone2ID))


    
    T0.start()
    t0.start()
    time.sleep(1)
    t1.start()
    t2.start()

    T0.join()
    t0.join()
    t1.join()
    t2.join()
    

  
if __name__ == "__main__":
   
    
    build_conn()  #starts camera file and drone1 file , also builds connection btw the two

