from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message


class Drone():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.Message = Message()

    def takeOff(self):
        self.sendData(self.Message.command(1), "takeOff")

    def land(self):
        self.sendData(self.Message.command(2), "Land")

    # def backFlip(self):
    #     self.sendData(self.Message.command(3), "BackFlip")

    # def frontFlip(self):
    #     self.sendData(self.Message.command(4), "frontFlip")

    # def rightFlip(self):
    #     self.sendData(self.Message.command(5), "rightFlip")

    # def leftFlip(self):
    #     self.sendData(self.Message.command(6), "LeftFlip")
    
    def forward(self):
        self.sendData(self.Message.move("forward"), "Forward")

    def backward(self):
        self.sendData(self.Message.move("backward"), "Backward")
    
    def left(self):
        self.sendData(self.Message.move("left"), "Left")
    
    def right(self):
        self.sendData(self.Message.move("right"), "Right")
        
    def up(self):
        self.sendData(self.Message.move("up"), "Up")
        
    def down(self):
        self.sendData(self.Message.move("down"), "Right")
    
    def clockwise(self):
        self.sendData(self.Message.move("clck"), "Clockwise")
        
    def anticlockwise(self):
        self.sendData(self.Message.move("anticlck"), "Anticlockwise")
    
    def arm(self):
        self.sendData(self.Message.arming(True), "ARM")

    def disArm(self):
        self.sendData(self.Message.arming(False), "Disarm")
        
    def getIMU(self):
        self.sendData(self.Message.move("IMU"), "IMU")

    def sendData(self, data, err):
        try:
            print("Sent data: ", end="")
            print(data)
            self.conn.write(data)
            print("ReadVeryEager data: ", end="")
            recd = self.conn.read_very_eager()
            print(recd)
            print("Decoded data: ", self.Message.decode(recd))
        except:
            print("Error While sending {} Data".format(err))


