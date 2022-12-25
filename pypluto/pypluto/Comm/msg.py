import struct
from pypluto.Comm.packets import *

MSP_SET_COMMAND = 217   # in cmd used for predefined commands
MSP_SET_RAW_RC = 200    # in cmd 8 rc channel
class Message():
    def __init__(self):
        self.HEADER = [b'$', b'M']
        self.DIRECTION = {"IN": b'<', "OUT": b'>'}  # IN: to Drone OUT: From Drone
        self.MSP_MSG_PARSE = '<3c2B%iHB'
    
    def parse(self, data, typeOfMsg):
        print("Data = " , data)
        lenOfData = len(data)
        msg = self.HEADER + [self.DIRECTION["IN"]] + [lenOfData * 2] + [typeOfMsg] + data
        print(msg)
        msg = struct.pack(self.MSP_MSG_PARSE[:-1] % lenOfData, *msg)

        # Checksum calc is XOR between <size>, <command> and (each byte) <data>
        checksum = 0
        for i in msg[3:]:
            checksum ^= i
        # Add checksum at the end of the msg
        msg += bytes([checksum])
        return msg

    def set_command(self, cmd):
        return self.parse([cmd], MSP_SET_COMMAND)

    def set_raw_rc(self, data):
        return self.parse(data, MSP_SET_RAW_RC)

    





