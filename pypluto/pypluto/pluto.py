from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
import numpy as np


class Drone():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.msg = Message()

    def takeOff(self):
        self.sendData(self.msg.set_command(1), "takeOff")

    def land(self):
        self.sendData(self.msg.set_command(2), "Land")

    def backFlip(self):
        self.sendData(self.msg.set_command(3), "BackFlip")

    def frontFlip(self):
        self.sendData(self.msg.set_command(4), "frontFlip")

    def rightFlip(self):
        self.sendData(self.msg.set_command(5), "rightFlip")

    def leftFlip(self):
        self.sendData(self.msg.set_command(6), "LeftFlip")
    
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
            speed = arg

        change = {
            "forward": np.array([0, speed, 0, 0]),
            "backward": np.array([0, -speed, 0, 0]),      
            "left": np.array([-speed, 0, 0, 0]),      
            "right": np.array([speed, 0, 0, 0]),
            "up": np.array([0, 0, 0, speed]),
            "down": np.array([0, 0, 0, -speed]),
            "Y": np.array([0, speed, 0, 0]),
            "X": np.array([speed, 0, 0, 0]),
            "Z": np.array([0, 0, 0, speed])
        }
        
        RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE,  = center + change[direction]
        data = [RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        self.sendData(self.msg.set_raw_rc(data),"Move")

    def arm(self):
        self.arming(True)

    def disarm(self):
        self.arming(False)


    def sendData(self, data, err):
        try:
            self.conn.write(data)
        except:
            print("Error While sending {} Data".format(err))
    


