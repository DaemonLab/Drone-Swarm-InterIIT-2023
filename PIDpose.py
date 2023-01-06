import numpy as np
import time
from marker import Aruco
import cv2

class Position:

    Kpx = 0.05
    KIx = 0
    KDx = 0

    Kpy = 0.05
    KIy = 0
    KDy = 0

    def __init__(self,drone):
        self.currentVec = np.array([0.0, 0.0])  # (X, Y, Z)
        self.desiredVec = np.array([0.0, 0.0])  # (targetX, targetY, targetZ)
        self.previousErr = np.array([0.0, 0.0]) 
        self.integralErr = np.array([0.0, 0.0])  
        self.drone = drone
        self.cap = cv2.VideoCapture(2)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    
    def PIDcontrol(self, dt):

        Err = self.desiredVec - self.currentVec
        errx, erry = Err
        # terms = np.vstack((
        #     Err,
        #     (Err-self.previousErr)/dt,
        #     self.integralErr
        #     ))
        # command = np.sum(np.dot(terms, self.KPID), axis=0)


        
        command = np.array([self.Kpx*errx, self.Kpy*erry])
        self.previousErr = Err
        self.integralErr += Err*dt

        return command

    def go_to(self, desiredVec):
        self.desiredVec = np.array(desiredVec) # in [pixels, pixels]
        
        aruco = Aruco("DICT_4X4_50")

        prev_time = time.time() - 0.1 # to avoid divide by zero

        while self.cap.isOpened():
            try:
            
                # current_time = time.time()
                _, image = self.cap.read()
                corners, ids, rejected = aruco.detectMarkers(image)
                # detected_markers = aruco.display(corners, ids, image, desiredVec)

                pose, is_detected, detected_markers = aruco.get_pose(corners, ids, image, desiredVec, display=True)
                # cv2.imshow("Image", detected_markers)
                if is_detected:
                    x, y, _ = pose
                    self.currentVec = np.array([x,y]) # [pixels, pixels, altitude in cm]
                    self.previousErr = self.desiredVec - self.currentVec
                    if np.linalg.norm(self.previousErr[:2])<20 and abs(self.previousErr[2])<5:
                        print("Target Reached")
                        self.drone.disarm()
                        break

                    else:
                        dt = 0.1
                        roll, pitch = self.PIDcontrol(dt) 
                        yaw = 0

                        # apply commands
                        self.drone.trim(int(roll), int(-pitch), 0, 0)
                        time.sleep(0.1)
                        print(f"Sent roll: {int(roll)} and pitch: {int(-pitch)}")

                        

                else:
                    print('Aruco not detected')


                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("Camera feed lost. Stabilizing...")
                    self.drone.speedx(0)
                    self.drone.speedy(0)
                    break
            except KeyboardInterrupt:
                print("Stopped. Keyboard Interrupt")
                break

        
        


