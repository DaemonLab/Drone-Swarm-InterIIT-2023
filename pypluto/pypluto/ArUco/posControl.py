from marker import Aruco
import numpy as np

class Position:

    # to be tuned
    KPx = 1.0
    KIx = 0
    KDx = 0
    KPy = 1.0
    KIy = 0
    KDy = 0

    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.yaw = np.pi/2
        self.desiredX = 0.0
        self.desiredY = 0.0
        self.desiredZ = 0.0
        self.coordinates = {
            "X":(self.X,self.desiredX),
            "Y":(self.Y,self.desiredX)
        }        
        

    def get_pose(self,image):
        aruco = Aruco("DICT_5X5_50")
        pose,is_detected = aruco.get_pose(image)
        if is_detected:
            self.X, self.Y, self.yaw = pose
    
    def PIDcontrol(self, axis):
        


