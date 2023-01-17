
import socket
import time
import math

MSP_STATUS=101          # out cmd cycletime & errors_count & sensor present & box activation & current setting number
MSP_RAW_IMU=102         # 9 DOF 
MSP_ATTITUDE=108        # 2 angles 1 heading
MSP_ALTITUDE=109        # altitude, variometer
MSP_ANALOG=110          # vbat, powermetersum, rssi if available on RX

MSP_SET_RAW_RC=200      # 8 rc channel
MSP_SET_COMMAND=217     # setting commands 

class pluto:
   
    def __init__(self, DroneIP="192.168.4.1", DronePort=23):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.BUFFER_SIZE = 1024
       
        self.roll=1500                    
        self.pitch=1500                 
        self.throttle=1500 
        self.yaw=1500                      
        self.aux1=1200
        self.aux2=1000
        self.aux3=1500
        self.aux4=1200
        
        self.buffer_rc=bytearray([])               # rc data that has to be sent continuously 
        self.set=False
        self.trim(0,0,0,0)
    
    def setzero(self):
        self.set=True


    def connect(self):
        try:
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mySocket.connect((self.DRONEIP, self.DRONEPORT))
            print("pluto connected")
        except:
            print("Cannot connect to pluto, please try again...")

    def disconnect(self):
        self.mySocket.close()
        print("pluto disconnected")

    def trim(self,Roll,Pitch,Throttle,Yaw):
        
        Roll=max(-100,min(Roll,100))
        Pitch=max(-100,min(Pitch,100))
        Throttle=max(-100,min(Throttle,100))
        Yaw=max(-100,min(Yaw,100))

        self.roll=1500 + Roll
        self.pitch=1500 + Pitch
        self.throttle=1500 + Throttle
        self.yaw=1500 + Yaw
        
        self.rc=[self.roll, self.pitch, self.throttle, self.yaw, self.aux1, self.aux2, self.aux3, self.aux4]
    
       
    def create_sendMSPpacket(self, msg_type, msg):
        self.buffer=bytearray([])                   # data to be sent
        headerArray=bytearray([36,77,60])           # header array "$","M","<"
        self.buffer.extend(headerArray)
        msg_len=2*len(msg)
        self.buffer.append(msg_len)
        self.buffer.append(msg_type)
        if(msg_len>0):
          for b in msg:
            LSB=b%256
            MSB=math.floor(b/256)
            self.buffer.append(LSB)
            self.buffer.append(MSB)
        CRCValue=0
        for b in self.buffer[3:]:
            CRCValue=CRCValue^b
        self.buffer.append(CRCValue)
    
        if(msg_type==200):
            self.buffer_rc=self.buffer[:]
            self.sendPacket(self.buffer)
        else:
            self.sendPacket(self.buffer_rc)
            self.sendPacket(self.buffer)
        

   

    def arm(self):   
        self.rc[2]=1000
        self.rc[-1]=1500
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(1)
       
    def disarm(self):
        self.rc[2]=1300
        self.rc[-1]=1200
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(1)
       


    def box_arm(self):
        self.rc[2]=1500
        self.rc[-1]=1500
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(0.5)
       

    def clamp_rc(self,x:int):
        return max(1000, min(2000,x))

    def speedx(self,value,duration=0):  
       
        no_of_loops=10*duration 
        self.rc[0]=self.clamp_rc(self.roll + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
            #print(self.rc)
           
  
        
    def speedy(self,value,duration=0):  
        no_of_loops=10*duration 
        self.rc[1]=self.clamp_rc(self.pitch + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
            #print(self.rc)
           

    def speedz(self,value,duration=0): 
        no_of_loops=10*duration 
        self.rc[2]=self.clamp_rc(self.throttle + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
            #print(self.rc)

    def rotate(self,value,duration=0): 
        no_of_loops=10*duration 
        self.rc[3]=self.clamp_rc(self.yaw + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
            #print(self.rc)
           

    def takeoff(self):
        self.box_arm()
        cmd=[1]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.speedz(0,3)
        
        
    def land(self):
        cmd=[2]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.speedz(0,5)


    def flip(self):
        cmd=[3]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.speedz(0,3)

    
    def get_height(self,duration=0):
        no_of_loops=10*duration
        while(no_of_loops>0):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 & data[4]==109):
                print(data[-2])
            no_of_loops=no_of_loops-1
            time.sleep(0.1)
        if(duration==0):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 & data[4]==109):
                print(data[-3])
           
    def get_vario(self,duration=0):
        no_of_loops=10*duration
        while(no_of_loops>0):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 and data[4]==109):
                print(data[-3] if data[-2]==0 else data[-3]-255)
            no_of_loops=no_of_loops-1
            time.sleep(0.1)
        if(duration==0):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 and data[4]==109):
                print(data[-3] if data[-2]==0 else data[-3]-255)
    

    def get_roll(self,duration=0):
        no_of_loops=10*duration
        while(no_of_loops>0):
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 and data[4]==108):
                #print(data[5] if data[6]==0 else data[5]-255)
                print(data[6])
            no_of_loops=no_of_loops-1
            time.sleep(0.1)
        if(duration==0):
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            data=self.recievePacket()
            if(len(data)==12 and data[4]==108):
                print(data[5] if data[6]==0 else data[5]-255)


    def sendPacket(self,buff):
        #print(buff)
        self.mySocket.send(buff)

    def recievePacket(self):
        return self.mySocket.recv(self.BUFFER_SIZE)
    
    
