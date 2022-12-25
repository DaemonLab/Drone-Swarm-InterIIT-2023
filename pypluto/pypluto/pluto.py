from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
from pypluto.commands.movement import Moving
import numpy as np


class Drone():
    
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.move_cmd = Moving()

    def arm(self):
        self.sendData(self.move_cmd.arming(True), "ARM")   
        
    def disarm(self):
        self.sendData(self.move_cmd.arming(False), "DISARM")

    def move(self, direction, *args):
        self.sendData(self.move_cmd.move(direction, *args), "MOVE")

    def sendData(self, data, err):
        try:
            print(data)
            self.conn.write(data)
        except:
            print("Error While sending {} Data".format(err))
