from pypluto.Comm.server import Connection
from pypluto.commands.mov_func import *


class Drone():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.msgType = MsgType()

    def takeOff(self):
        self.sendData(self.msgType.command(1), "takeOff")

    def land(self):
        self.sendData(self.msgType.command(2), "Land")

    # def backFlip(self):
    #     self.sendData(self.msgType.command(3), "BackFlip")

    # def frontFlip(self):
    #     self.sendData(self.msgType.command(4), "frontFlip")

    # def rightFlip(self):
    #     self.sendData(self.msgType.command(5), "rightFlip")

    # def leftFlip(self):
    #     self.sendData(self.msgType.command(6), "LeftFlip")
    
    def forward(self):
        self.sendData(self.msgType.move("forward"), "Forward")

    def backward(self):
        self.sendData(self.msgType.move("backward"), "Backward")
    
    def left(self):
        self.sendData(self.msgType.move("left"), "Left")
    
    def right(self):
        self.sendData(self.msgType.move("right"), "Right")
        
    def up(self):
        self.sendData(self.msgType.move("up"), "Up")
        
    def down(self):
        self.sendData(self.msgType.move("down"), "Right")
    
    def clockwise(self):
        self.sendData(self.msgType.move("clck"), "Clockwise")
        
    def anticlockwise(self):
        self.sendData(self.msgType.move("anticlck"), "Anticlockwise")
    
    def arm(self):
        self.sendData(self.msgType.arming(True), "ARM")

    def disArm(self):
        self.sendData(self.msgType.arming(False), "Disarm")
        
    def getIMU(self):
        self.sendData(self.msgType.get_data("IMU"), "IMU")

    def sendData(self, data, err):
        try:
            print(data)
            self.conn.write(data)
            print(self.conn.read_very_eager())
        except:
            print("Error While sending {} Data".format(err))