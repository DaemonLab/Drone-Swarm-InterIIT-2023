from pypluto import Connection
from pypluto import Message


class Drone():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.msg = Message()

    def takeOff(self):
        self.sendData(self.msg.command(1), "takeOff")

    def land(self):
        self.sendData(self.msg.command(2), "Land")

    def backFlip(self):
        self.sendData(self.msg.command(3), "BackFlip")

    def frontFlip(self):
        self.sendData(self.msg.command(4), "frontFlip")

    def rightFlip(self):
        self.sendData(self.msg.command(5), "rightFlip")

    def leftFlip(self):
        self.sendData(self.msg.command(6), "LeftFlip")
    
    def forward(self):
        self.sendData(self.msg.move("forward"), "Forward")

    def backward(self):
        self.sendData(self.msg.move("backward"), "Backward")
    
    def left(self):
        self.sendData(self.msg.move("left"), "Left")
    
    def right(self):
        self.sendData(self.msg.move("right"), "Right")

    def arm(self):
        self.sendData(self.msg.arming(True), "ARM")

    def disArm(self):
        self.sendData(self.msg.arming(False), "Disarm")

    def sendData(self, data, err):
        try:
            self.conn.write(data)
        except:
            print("Error While sending {} Data".format(err))
    


