from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
import numpy as np

def arming(self, arm: bool):
    L = 1000  # LOW
    C = 1500  # center
    H = 2000  # High
    RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = C, C, L, L, 1500, 1000, 1500, 1200
    data = [RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
    if arm:
        data[-1] = 1500
        self.sendData(self.msg.set_raw_rc(data),"ARM")
    else:
        data[-1] = 901
        self.sendData(self.msg.set_raw_rc(data),"DISARM")

    
def move(self, direction, *args):
    center = np.array([1500, 1500, 1500, 1500]) #RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE

    RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1500, 1500
    speed = 100
    for arg in args:
        speed = int(arg)
    
    if speed>2100:
        print("Clipping speed to 2100")
        speed = 2100
    if speed<900:
        print("Clipping speed to 900")
        speed = 900

    change = {
        "forward": np.array([0, speed, 0, 0]),
        "backward": np.array([0, -speed, 0, 0]),      
        "left": np.array([-speed, 0, 0, 0]),      
        "right": np.array([speed, 0, 0, 0]),
        "up": np.array([0, 0, 0, speed]),
        "down": np.array([0, 0, 0, -speed]),
        "clck": np.array([0, 0, speed, 0]),
        "anticlck": np.array([0, 0, -speed, 0]),
        "Y": np.array([0, speed, 0, 0]),
        "X": np.array([speed, 0, 0, 0]),
        "Z": np.array([0, 0, 0, speed])
    }
    
    RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE,  = center + change[direction]
    data = [RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
    self.sendData(self.msg.set_raw_rc(data),"Move")