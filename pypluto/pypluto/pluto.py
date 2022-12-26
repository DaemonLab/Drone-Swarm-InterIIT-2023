from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
from pypluto.commands.movement import Move
import numpy as np


class Drone():
    
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.move_cmd = Move()

    def arm(self):
        self.sendData(self.move_cmd.arming(True), "ARM")   
        
    def disarm(self):
        self.sendData(self.move_cmd.arming(False), "DISARM")

    def steer(self, direction:str, magnitude:int=100):
        """
        Steers the drone in the specified direction or angle.

        Parameters
        ----------
        direction : str
            Valid inputs - "forward", "backward", "left", "right", "up", "down", "pitch", "roll", "throttle" and "yaw".
        magnitude : int
            Magnitude over which the drone steers, -600<magnitude<600
        """
        self.sendData(self.move_cmd.steer_cmd(direction, magnitude), f"STEER {direction}")

    def sendData(self, data:bytes, err:str):
        try:
            print(data)
            self.conn.write(data)
        except:
            print("Error While sending {} Data".format(err))
