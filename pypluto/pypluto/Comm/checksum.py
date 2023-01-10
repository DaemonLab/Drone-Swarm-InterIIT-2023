import struct
from pypluto.Comm.cmdList import *

class Parse:
    def __init__(self):
        self.HEADER = [b'$', b'M']
        self.DIRECTION = {"IN": b'<', "OUT": b'>'}  # IN: to Drone OUT: From Drone
        self.MSP_MSG_PARSE = '<3c2B%iHB'

    def convert(self, data, typeOfMsg):
        lenOfData = len(data)
        if data==[]:
            msg = self.HEADER + [self.DIRECTION["IN"]] + [lenOfData * 2] + [102]
            print("Message to be packed: ", end="")
            print(msg)
            msg = struct.pack(self.MSP_MSG_PARSE[:-1] % 0, *msg)
        
        else:
            msg = self.HEADER + [self.DIRECTION["IN"]] + [lenOfData * 2] + [typeOfMsg] + data
            msg = struct.pack(self.MSP_MSG_PARSE[:-1] % lenOfData, *msg)
        
        print("Packed message: ", end="")
        print(struct.unpack(self.MSP_MSG_PARSE[:-1] % lenOfData , msg))

        print("Length of data: ", lenOfData)

        checksum = 0
        for i in msg[3:]:
            checksum ^= i

        print("Checksum: ", checksum)

        msg += bytes([checksum])
        return msg

    def decode(self, data):
        msg = struct.unpack(self.MSP_MSG_PARSE % 9, data)
        return msg
