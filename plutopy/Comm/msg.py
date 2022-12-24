import struct
import numpy as np

MSP_SET_COMMAND = 217   ## used for predefined commands
MSP_SET_RAW_RC = 200    ## 8 rc chennal

class Message():
    def __init__(self):
        self.HEADER = [b'$', b'M']
        self.DIRECTION = {"IN": b'<', "OUT": b'>'}  # IN: to Drone OUT: From Drone
        self.MSP_MSG_PARSE = '<3c2B%iHB'
    
    def parse(self, data, typeOfMsg):
        lenOfData = len(data)
        msg = self.HEADER + [self.DIRECTION["IN"]] + [lenOfData * 2] + [typeOfMsg] + data
        msg = struct.pack(self.MSP_MSG_PARSE[:-1] % lenOfData, *msg)

        # Checksum calc is XOR between <size>, <command> and (each byte) <data>
        checksum = 0
        for i in msg[3:]:
            checksum ^= i
        # Add checksum at the end of the msg
        msg += bytes([checksum])
        return msg

    def command(self, cmd):
        return self.parse([cmd], MSP_SET_COMMAND)

    def arming(self, arm: bool):
        L = 1000  # LOW
        C = 1500  # center
        H = 2000  # High
        RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = C, C, L, L, 1500, 1000, 1500, 1200
        data = [RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        if arm:
            data[-1] = 1500
            return self.parse(data, MSP_SET_RAW_RC)
        else:
            data[-1] = 901
            return self.parse(data, MSP_SET_RAW_RC)
    
        
    def move(self, direction, *args):
        center = np.array([1500, 1500, 1500, 1500]) #RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE

        RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4 = 1500, 1500, 1500, 1500
        speed = 100
        for arg in args:
            speed = arg
        
        ## refactor this with a dictionary:
        if direction=="forward":
            change = np.array([0, speed, 0, 0])
        
        if direction=="backward":
            change = np.array([0, -speed, 0, 0])
        
        if direction=="left":
            change = np.array([-speed, 0, 0, 0])
        
        if direction=="right":
            change = np.array([speed, 0, 0, 0])
        
        if direction=="up":
            change = np.array([0, 0, 0, speed])
        
        if direction=="down":
            change = np.array([0, 0, 0, -speed])

        if direction=="Y":
            change = np.array([0, speed, 0, 0])
        
        if direction=="X":
            change = np.array([speed, 0, 0, 0])

        if direction=="Z":
            change = np.array([0, 0, 0, speed])
        
        RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE,  = center + change
        data = [RC_ROLL, RC_PITCH, RC_YAW, RC_THROTTLE, RC_AUX1, RC_AUX2, RC_AUX3, RC_AUX4]
        return self.parse(data, MSP_SET_RAW_RC)





