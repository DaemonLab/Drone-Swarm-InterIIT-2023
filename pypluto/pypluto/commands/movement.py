from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
import numpy as np

class Move():

    def __init__(self):
        self.msg = Message()

    def arming(self, arm: bool):
        """
        Parses the arm and disarm commands.

        Parameters
        ----------
        arm : bool
            True for arm and False for disarm.
        Returns
        -------
        parsed : bytes
            The parsed data to be sent to the drone.
        """

        RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1000, 1700, 1500, 1000, 1500, 1500
        data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        if arm:
            data[-1] = 1500
        else:
            data[-1] = 901

        parsed = self.msg.set_raw_rc(data)
        return parsed
    
    
    '''
    def takeOff(self):
        data=[1]
        parsed=self.msg.set_command(data)
        return parsed

    def land(self):
         data=[2]
         parsed=self.msg.set_command(data)
         return parsed

    def backFlip(self):
        data=[3]
        parsed=self.msg.set_command(data)
        return parsed

    def frontFlip(self):
         data=[4]
         parsed=self.msg.set_command(data)
         return parsed

    def rightFlip(self):
         data=[5]
         parsed=self.msg.set_command(data)
         return parsed

    def leftFlip(self):
         data=[6]
         parsed=self.msg.set_command(data)
         return parsed
    '''  
     
    
    def steer_cmd(self, direction:str, magnitude:int=100):
        """
        Parses the steer commands.

        Parameters
        ----------
        direction : str
            Valid inputs - "forward", "backward", "left", "right", "up", "down", "pitch", "roll", "throttle" and "yaw".
        magnitude : int
            Magnitude over which the drone steers, -600<magnitude<600

        Returns
        -------
        parsed : bytes
            The parsed data to be sent to the drone.
        """

        center = np.array([1500, 1500, 1500, 1500])

        RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1500, 1500
    
        if magnitude + 1500 > 2100:
            print("Clipping magnitude to 2100")
            magnitude = 2100
        if magnitude + 1500 < 900:
            print("Clipping magnitude to 900")
            magnitude = 900

        change = {
            "forward": np.array([0, magnitude, 0, 0]),
            "backward": np.array([0, -magnitude, 0, 0]),      
            "left": np.array([-magnitude, 0, 0, 0]),      
            "right": np.array([magnitude, 0, 0, 0]),
            "up": np.array([0, 0, magnitude, 0]),
            "down": np.array([0, 0, -magnitude, 0]),
            "clck": np.array([0, 0, 0, magnitude]),
            "anticlck": np.array([0, 0, 0, -magnitude]),
            "roll": np.array([magnitude, 0, 0, 0]),
            "pitch": np.array([0, magnitude, 0, 0]),
            "throttle": np.array([0, 0, magnitude, 0]),
            "yaw": np.array([0, 0, 0, magnitude])
        }
    
        RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW,  = center + change[direction]
        data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        parsed = self.msg.set_raw_rc(data)
        return parsed
