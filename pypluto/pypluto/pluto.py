from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
from pypluto.commands.movement import Move
import numpy as np
import subprocess
import time
from multiprocessing import Process,Queue,Pipe
from pypluto.commands.OUT_STREAM import out_stream

parent_conn,child_conn = Pipe()

class Drone():
    
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        global parent_conn,child_conn
        a = out_stream()
        p = Process(target=a.getData, args=(child_conn,))
        p.start()

        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.move_cmd = Move()
        

    def arm(self):
        self.sendData(self.move_cmd.arming(True), "ARM")   
        
    def disarm(self):
        self.sendData(self.move_cmd.arming(False), "DISARM")

    def steer(self, direction:str, magnitude:int=100):
        self.sendData(self.move_cmd.steer_cmd(direction, magnitude), f"STEER {direction}")
    
    def set_steer(self, magnitude):
        if len(magnitude) != 4:
            print("Invalid legth of message array. format: [roll, pitch, throttle, yaw]")
        self.sendData(self.move_cmd.set_steer_data(magnitude), f"Sending {magnitude}")

    def takeoff(self):
        self.sendData(self.move_cmd.takeoff() , "TAKEOFF")

    def sendData(self, data:bytes, err:str):
        global parent_conn,child_conn
        if(True):
            print(data)
            parent_conn.send(data)