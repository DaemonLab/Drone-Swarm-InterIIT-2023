from pypluto.Comm.checksum import *
from pypluto.Comm.cmdList import *

#Each message has its own type of input/payload... this file handles them seperately

class Message():
    def __init__(self):
        self.parse = Parse()

    def command(self, cmd):
        return self.parse.convert([cmd], MSP_SET_COMMAND)

    def arming(self, arm: bool):
        RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1000, 1500, 1500, 1000, 1500, 1500
        data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        if arm:
            data[-1] = 1500
            return self.parse.convert(data, MSP_SET_RAW_RC)
        else:
            data[-1] = 901
            return self.parse.convert(data, MSP_SET_RAW_RC)
    
    def move(self, cmd):
        RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1500, 1500

        if cmd=="right":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1600, 1500, 1500, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        
        if cmd=="left":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1400, 1500, 1500, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        
        if cmd=="backward":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1400, 1500, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        
        if cmd=="forward":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1600, 1500, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
            
        if cmd=="up":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1500, 1800, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
            
        if cmd=="down":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1500, 1300, 1500
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        
        if cmd=="clck":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1500, 1500, 1600
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
            
        if cmd=="anticlck":
            RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW  = 1500, 1500, 1500, 1400
            data = [RC_ROLL, RC_PITCH, RC_THROTTLE, RC_YAW, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        
        if cmd=="IMU":
            data = []
        
        return self.parse.convert(data, MSP_SET_RAW_RC)

    def decode(self, data):
        return self.parse.decode(data)