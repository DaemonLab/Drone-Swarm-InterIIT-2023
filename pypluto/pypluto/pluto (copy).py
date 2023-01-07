from pypluto.Comm.server import Connection
from pypluto.Comm.msg import Message
from pypluto.commands.movement import Move
import numpy as np
import subprocess
import time
from multiprocessing import Process,Queue,Pipe
from pypluto.commands.OUT_STREAM import out_stream



class Drone():
    
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        parent_conn,child_conn = Pipe()
        a = out_stream()
        p = Process(target=a.sendMsg, args=(child_conn,))
        p.start()
        a.arm()
        a.sendMsg(child_conn)
        time.sleep(5)
        while(parent_conn.poll()):
            print(parent_conn.recv())
        
        a.arm()
        time.sleep(5)
        
        #while(parent_conn.poll()):
        #    print(parent_conn.recv())
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.conn = Connection(self.DRONEIP, self.DRONEPORT).connect()
        self.move_cmd = Move()
        

    def arm(self):
        self.sendData(self.move_cmd.arming(True), "ARM")   
        
    def disarm(self):
        self.sendData(self.move_cmd.arming(False), "DISARM")

    def steer(self, direction:str, magnitude:int=100):
        """
        Steers the drone in the specified direction.

        Parameters
        ----------
        direction : str
            Valid inputs - "forward", "backward", "left", "right", "up", "down".
        magnitude : int
            Magnitude over which the drone steers, -600<magnitude<600
        """
        self.sendData(self.move_cmd.steer_cmd(direction, magnitude), f"STEER {direction}")
    
    def set_steer(self, magnitude):
        """
        Changes the msg data.

        Parameters
        ----------
        magnitude : array-like
            Magnitude of roll, pitch, throttle, and yaw commands -600<magnitude<600
        """
        if len(magnitude) != 4:
            print("Invalid legth of message array. format: [roll, pitch, throttle, yaw]")
        self.sendData(self.move_cmd.set_steer_data(magnitude), f"Sending {magnitude}")

    def takeoff(self):
        self.sendData(self.move_cmd.takeoff() , "TAKEOFF")

    def sendData(self, data:bytes, err:str):
        try:
            print(data)
            self.conn.write(data)
        except:
            print("Error While sending {} Data".format(err))
