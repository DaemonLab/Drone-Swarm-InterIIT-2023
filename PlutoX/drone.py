import telnetlib
import time
import math

class pluto:
   
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.raw_rc_array=bytearray([36,77,60,16,200,220,5,220,5,220,5,220,5,176,4,232,3,220,5,176,4,234])
        self.set_command_array=bytearray([36,77,60,2,217,0,0,0])
        self.roll=1500                    
        self.pitch=1500                 
        self.throttle=1500 
        self.yaw=1500                      
        self.aux1=1200
        self.aux2=1000
        self.aux3=1500
        self.aux4=1200
        self.set=False
        self.temp=bytearray([])
        self.trim(0,0,0,0)
    
    def setzero(self):
        self.set=True


    def connect(self):
        try:
            self.tn=telnetlib.Telnet(self.DRONEIP,self.DRONEPORT)
            print("pluto connected")
        except:
            print("Cannot connect to pluto, please try again...")

    def disconnect(self):
        self.tn.close()
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
        
        arr=bytearray([])
        arr.extend(self.getBytes(self.roll))
        arr.extend(self.getBytes(self.pitch))
        arr.extend(self.getBytes(self.throttle))
        arr.extend(self.getBytes(self.yaw))
        self.raw_rc_array[5]=arr[0]
        self.raw_rc_array[6]=arr[1]
        self.raw_rc_array[7]=arr[2]
        self.raw_rc_array[8]=arr[3]
        self.raw_rc_array[9]=arr[4]
        self.raw_rc_array[10]=arr[5]
        self.raw_rc_array[11]=arr[6]
        self.raw_rc_array[12]=arr[7]
        self.raw_rc_array[19]=220
        self.raw_rc_array[20]=5
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        self.temp=self.raw_rc_array[:]
       


    def changeCRC(self,arr):
        self.CRCArray=arr[3:-1]
        self.CRCValue=0
        for d in self.CRCArray:
            self.CRCValue= self.CRCValue^d
        return self.CRCValue
    
    def getBytes(self,value): 
        self.LSB=value % 256
        self.MSB=math.floor(value/256)
        return bytearray([self.LSB,self.MSB])

    def arm(self):   
        self.raw_rc_array[19]=220
        self.raw_rc_array[20]=5
        self.raw_rc_array[9]=232
        self.raw_rc_array[10]=3
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        self.tn.write(self.raw_rc_array)
        print(self.raw_rc_array)
        time.sleep(1)


    def disarm(self):
        self.raw_rc_array[19]=176
        self.raw_rc_array[20]=4
        self.raw_rc_array[9]=20
        self.raw_rc_array[10]=5
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        self.tn.write(self.raw_rc_array)
        print(self.raw_rc_array)
        time.sleep(1)

    def clamp_rc(self,x:int):
        return max(1000, min(2000,x))

    def speedx(self,value,duration=0):  
        if(self.set):
            self.raw_rc_array=self.temp[:]
        no_of_loops=2*duration 
        rc_roll=self.clamp_rc(self.roll + 5*value)    
        arr=bytearray([])
        arr.extend(self.getBytes(rc_roll))
        #print(arr)
        self.raw_rc_array[5]=arr[0]
        self.raw_rc_array[6]=arr[1]
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        while(no_of_loops>0):
         self.tn.write(self.raw_rc_array)
         print(self.raw_rc_array)
         no_of_loops=no_of_loops-1
         time.sleep(0.5)
        if(duration==0):
            self.tn.write(self.raw_rc_array)
            #print(self.raw_rc_array)
            #time.sleep(0.1)
  
        
    def speedy(self,value,duration=0):  
        if(self.set):
            self.raw_rc_array=self.temp[:]
        no_of_loops=2*duration    
        rc_pitch=self.clamp_rc(self.pitch + 5*value)   
        arr=bytearray([])
        arr.extend(self.getBytes(rc_pitch))
        self.raw_rc_array[7]=arr[0]
        self.raw_rc_array[8]=arr[1]
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        while(no_of_loops>0):
         self.tn.write(self.raw_rc_array)
         print(self.raw_rc_array)
         no_of_loops=no_of_loops-1
         time.sleep(0.5)
        if(duration==0):
            self.tn.write(self.raw_rc_array)
            #print(self.raw_rc_array)
            #time.sleep(0.1)

    def speedz(self,value,duration=0): 
        if(self.set):
            self.raw_rc_array=self.temp[:]
        no_of_loops=2*duration    
        rc_throttle=self.clamp_rc(self.throttle + 5*value)   
        arr=bytearray([])
        arr.extend(self.getBytes(rc_throttle))
        self.raw_rc_array[9]=arr[0]
        self.raw_rc_array[10]=arr[1]
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        while(no_of_loops>0):
         self.tn.write(self.raw_rc_array)
         print(self.raw_rc_array)
         no_of_loops=no_of_loops-1
         time.sleep(0.5)
        if(duration==0):
            self.tn.write(self.raw_rc_array)
            #print(self.raw_rc_array)
            #time.sleep(0.5)

    def rotate(self,value,duration=0): 
        if(self.set):
            self.raw_rc_array=self.temp[:]
        no_of_loops=2*duration  
        rc_yaw=self.clamp_rc(self.yaw + 5*value)     
        arr=bytearray([])
        arr.extend(self.getBytes(rc_yaw))
        self.raw_rc_array[11]=arr[0]
        self.raw_rc_array[12]=arr[1]
        Val=self.changeCRC(self.raw_rc_array)
        self.raw_rc_array[21]=Val
        while(no_of_loops>0):
         self.tn.write(self.raw_rc_array)
         print(self.raw_rc_array)
         no_of_loops=no_of_loops-1
         time.sleep(0.5)
        if(duration==0):
            self.tn.write(self.raw_rc_array)
            #print(self.raw_rc_array)
            #time.sleep(0.5)

    def takeoff(self):
        self.speedz(0)
        self.set_command_array[5]=1
        self.set_command_array[6]=0
        Val=self.changeCRC(self.set_command_array)
        self.set_command_array[7]=Val
        self.tn.write(self.set_command_array)
        print(self.set_command_array)
        self.speedz(1,3)
        
    def land(self):
        self.set_command_array[5]=2
        self.set_command_array[6]=0
        Val=self.changeCRC(self.set_command_array)
        self.set_command_array[7]=Val
        self.tn.write(self.set_command_array)
        print(self.set_command_array)
        self.speedz(0,7)

    def flip(self):
        self.set_command_array[5]=3
        self.set_command_array[6]=0
        Val=self.changeCRC(self.set_command_array)
        self.set_command_array[7]=Val
        self.tn.write(self.set_command_array)
        print(self.set_command_array)
        self.speedz(0,3)

    
    
    
