from ast import literal_eval
from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
import numpy as np
import time

msg_rc = b'$M<\x10\xc8\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xb0\x04\xe8\x03\xdc\x05\xb0\x04\xea'      #put message after setting 1500,1500,1200,1500,1500,1500,1500,1500
#msg_rc = b'$M<\x10\xc8\xdc\x05\xdc\x05\xe8\x03\xa4\x06\xdc\x05\xe8\x03\xdc\x05\xdc\x05\xa3'
msg_set_cmd = "D_cmd"

flag_set_cmd = False
flag_imu = False
flag_attitude = False
flag_altitude = False
flag_ACC_CALIB = False
flag_MAG_CALIB = False
flag_SET_TRIM = False

msg_imu = ""      #put the IMU send msg here
msg_attitude = ""      #put the attitude send msg here
msg_altitude = ""      #put the altitude send msg here
msg_ACC_CALIB = ""      #put the ACC_CALIB send msg here
msg_MAG_CALIB = ""      #put the MAG_CALIB send msg here
msg_SET_TRIM = ""      #put the SET_TRIM send msg here
data = []

t_set_cmd = time.time()

class out_stream():
    
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        print(DroneIP , DronePort)
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        
    
    def getData(self, child_conn):     #Make async if too slow
        global msg_rc
        global msg_set_cmd
        global flag_set_cmd
        global flag_imu
        global flag_attitude
        global flag_altitude
        global flag_ACC_CALIB
        global flag_MAG_CALIB
        global flag_SET_TRIM
        while(True):
            while not child_conn.poll():     #Might want a do-while loop instead
                #print(msg_rc[9],msg_rc[10])
                self.conn.write(msg_rc)
                time.sleep(0.1)
                if flag_set_cmd:
                    self.conn.write(msg_set_cmd)
                    
                if flag_imu:
                    self.conn.write(msg_imu)
                    
                if flag_attitude:
                    self.conn.write(msg_attitude)
                    
                if flag_altitude:     #Put flags into bool sections to reduce computation
                    self.conn.write(msg_altitude)
                
                if flag_ACC_CALIB:
                    self.conn.write(msg_ACC_CALIB)
                    flag_ACC_CALIB = False
                    
                if flag_MAG_CALIB:
                    self.conn.write(msg_MAG_CALIB)
                    flag_MAG_CALIB = False
            self.parseData(child_conn)
        
    def parseData(self, child_conn):
        data = child_conn.recv()
        global msg_rc
        global msg_set_cmd
        global flag_set_cmd
        global flag_imu
        global flag_attitude
        global flag_altitude
        
        if(data[4] == 200):
            msg_rc = data
            
        elif(data[4] == 217):
            msg_set_cmd = data
            flag_set_cmd = True
            
        elif(data[4] == 102):   #Flags should always be at the end to reduce number of checks
            flag_imu = True
            
        elif(data[4] == 108):
            flag_attitude = True
            
        elif(data[4] == 109):
            flag_altitude = True
            
        elif(data[4] == 205):
            global flag_ACC_CALIB
            flag_ACC_CALIB = True
            
        elif(data[4] == 206):
            global flag_MAG_CALIB
            flag_MAG_CALIB = True
            
        elif(data[4] == 239):
            global flag_SET_TRIM
            flag_SET_TRIM = True
