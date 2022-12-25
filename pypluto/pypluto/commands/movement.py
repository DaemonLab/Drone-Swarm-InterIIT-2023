from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
import numpy as np

class Moving():

    def __init__(self):
        self.msg = Message()

    def arming(self, arm: bool):
        RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1000, 1700, 1500, 1000, 1500, 1500
        data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        if arm:
            data[-1] = 1500
            return (self.msg.set_raw_rc(data))
        else:
            data[-1] = 901
            return (self.msg.set_raw_rc(data))

    
    def move(self, direction, *args):
        center = np.array([1500, 1500, 1500, 1500])

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
    
        RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW,  = center + change[direction]
        data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        return (self.msg.set_raw_rc(data))
