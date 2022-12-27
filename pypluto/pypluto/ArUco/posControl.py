import numpy as np
import time
from marker import Aruco
import cv2
from CAM_CONFIGS import *

class Position:

    KPID = np.array([
        [1.0, 1.0, 1.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ])
    def __init__(self,client):
        self.currentVec = np.array([0.0, 0.0, 0.0])  # (X, Y, Z)
        self.desiredVec = np.array([0.0, 0.0, 0.0])  # (targetX, targetY, targetZ)
        self.previousErr = np.array([0.0, 0.0, 0.0]) 
        self.integralErr = np.array([0.0, 0.0, 0.0])  
        self.client = client    

    
    def PIDcontrol(self, dt):

        Err = self.desiredVec - self.currentVec
        terms = np.vstack((
            Err,
            (Err-self.previousErr)/dt,
            self.integralErr
            ))
        command = np.sum(np.dot(terms, self.KPID), axis=0)
        

        self.previousErr = Err
        self.integralErr += Err*dt

        return command

    def go_to(self, desiredVec):
        self.desiredVec = desiredVec # in [pixels, pixels, altitude in cm]
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        prev_time = time.time() - 0.1 # to avoid divide by zero
        while cap.isOpened():
            
            current_time = time.time()
            _, image = cap.read()
            aruco = Aruco("DICT_5X5_50")
            corners, ids, rejected = aruco.detectMarkers(image)
            x,y,z,_ = aruco.get_pose(corners, ids, matrix_coefficients=MATRIX_COEFFS, distortion_coefficients=DIST_COEFFS)
            self.currentVec = np.array([x,y,z]) # [pixels, pixels, altitude in cm]
            self.previousErr = self.desiredVec - self.currentVec
            if np.linalg.norm(self.previousErr[:2])<10 and abs(self.previousErr[2])<5:
                print("Target Reached")
            else:
                dt = current_time - prev_time
                roll, pitch, throttle = self.PIDcontrol(dt) 
                yaw = 0

                # apply commands
                self.client.set_steer([roll, pitch, throttle, yaw])

                prev_time = current_time

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Camera feed lost. Stabilizing...")
                roll, pitch, throttle, yaw = 0, 0, 0, 0
                self.client.set_steer([roll, pitch, throttle, yaw])
                break


        
        


