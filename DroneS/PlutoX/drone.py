import socket
import time
import math
import sys
from select import select
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty



MSP_STATUS=101          # out cmd cycletime & errors_count & sensor present & box activation & current setting number
MSP_RAW_IMU=102         # 9 DOF 
MSP_ATTITUDE=108        # 2 angles 1 heading
MSP_ALTITUDE=109        # altitude, variometer
MSP_ANALOG=110          # vbat, powermetersum, rssi if available on RX

MSP_SET_RAW_RC=200      # 8 rc channel
MSP_SET_COMMAND=217     # setting commands 
RETRY_COUNT=5           # no of retries before getting required data
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
        self.trim(0,0,0,0)
        

    

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

    def roll_speed(self,value,duration=0):  
       
        no_of_loops=10*duration 
        self.rc[0]=self.clamp_rc(self.roll + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
           
  
        
    def pitch_speed(self,value,duration=0):  
        no_of_loops=10*duration 
        self.rc[1]=self.clamp_rc(self.pitch + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)

           

    def throttle_speed(self,value,duration=0): 
        no_of_loops=10*duration 
        self.rc[2]=self.clamp_rc(self.throttle + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        

    def yaw_speed(self,value,duration=0): 
        no_of_loops=10*duration 
        self.rc[3]=self.clamp_rc(self.yaw + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
           
    def reset_speed(self):
        self.rc[:4]=[self.roll,self.pitch,self.throttle,self.yaw]
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)


    def takeoff(self):
        self.box_arm()
        cmd=[1]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,3)
        
        
    def land(self):
        cmd=[2]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,5)
        self.disarm()


    def flip(self):
        cmd=[3]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,3)

    

    def read16(self,arr):
        if((arr[1]&0x80) ==0):
            return ((arr[1] << 8) + (arr[0]&0xff))             # for positive values 
        else:
            return (-65535 + (arr[1] << 8) + (arr[0]&0xff))    # for negative values

    
    ################################################## MSP_ALTITUDE #############################################################

    def get_height(self):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            for i in range(5):
             data=self.recievePacket()
             if(len(data)==12 & data[4]==109):
               return self.read16(data[5:7])


    def get_vario(self):
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==12 & data[4]==109):
              return self.read16(data[-3:-1])


    
    ###################################################### MSP_ATTITUDE #########################################################

    def get_roll(self):
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==12 and data[4]==108):
                return self.read16(data[5:7])/10
  

    def get_pitch(self):
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==12 and data[4]==108):
                return self.read16(data[7:9])/10
    

    def get_yaw(self):
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==12 and data[4]==108):
                return self.read16(data[9:11])


    ###################################################### MSP_RAW_IMU ##########################################################
    
    def get_acc_x(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[5:7])


    def get_acc_y(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[7:9])
    

    def get_acc_z(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[9:11])
    

    def get_gyro_x(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[11:13])
    

    def get_gyro_y(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[13:15])
    

    def get_gyro_z(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[15:17])
    

    def get_mag_x(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[17:19])
    

    def get_mag_y(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[19:21])
 

    def get_mag_z(self):
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             if(len(data)==24 and data[4]==102):
                return self.read16(data[21:23])


###################################################### MSP_ANALOG ###############################################################

    def get_battery(self):
            data=[]
            self.create_sendMSPpacket(MSP_ANALOG,data) 
            data=self.recievePacket()
            if(len(data)>5 and data[4]==110):
                return data[5]/10
   


    def sendPacket(self,buff):
        #print(buff)
        self.mySocket.send(buff)

    def recievePacket(self):
        return self.mySocket.recv(self.BUFFER_SIZE)
    
    
###################################################### KEYBOARD_CONTROL #########################################################

    
    def getKey(self,settings):
        """
        Function Name: getKey
        Input: None
        Output: keyboard charecter pressed
        Logic: Determine the keyboard key pressed
        Example call: getkey()
        """
        
        if sys.platform == 'win32':
            # getwch() returns a string on Windows
            key = msvcrt.getwch()
            print("Key sent from Windows: '", key, "'")
        else:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
                if (key == '\x1b'): # \x1b is Escape key
                    key = sys.stdin.read(2)
                sys.stdin.flush()
            else:
                key = ''

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
            print("Key sent from Linux: ", key)
        return key
        
    def saveTerminalSettings(self):
        if sys.platform == 'win32':
            return None
        return termios.tcgetattr(sys.stdin)

    def restoreTerminalSettings(self,old_settings):
        if sys.platform == 'win32':
            return termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def indentify_key(self,key_value):

        if key_value == 70:
            if self.armed:
                self.disarm()
                self.armed = not self.armed
            else:
                self.arm()
                self.armed = not self.armed

        elif key_value == 10:
            print("Forward key detected")
            self.pitch_speed(200) # forward

        elif key_value == 30:
            print("Left key detected")
            self.roll_speed(-200) # left

        elif key_value == 40:
            print("Right key detected")
            self.roll_speed(200) # right

        elif key_value == 80:
            self.reset_speed()

        elif key_value == 50:
            self.throttle_speed(400) # increase height

        elif key_value == 60:
            self.throttle_speed(-200) # decrease_height

        elif key_value == 110:
            print("Backward key detected")
            self.pitch_speed(-200) # backwards

        elif key_value == 130:
            self.takeoff()

        elif key_value == 140:
            self.land()

        elif key_value == 150:
            self.yaw_speed(-300) # yaw left

        elif key_value == 160:
            self.yaw_speed(300) # yaw right
    
        elif key_value == 42: # windows special key
            key2 = msvcrt.getwch()
            print("Special key detected: ", key2)
            
            # check for windows special key type
            if key2 == 'H': # up arrow
                print("Forward key detected")
                self.pitch_speed(200) # forward

            elif key2 == 'K': # left arrow
                print("Left key detected")
                self.roll_speed(-200) # left

            elif key2 == 'M': # right arrow'
                print("Right key detected")
                self.roll_speed(200) # right

            elif key2 == 'P': # down arrow
                print("Backward key detected")
                self.pitch_speed(-200)
        

    def keyboard_control(self,stat=False):
        
        self.disarm()
        self.armed = False
        msg="""   
            Control Your Drone!
            ---------------------------
            spacebar : arm or disarm
            w : increase height
            s : decrease height
            q : take off
            e : land
            a : yaw left
            d : yaw right
            Up arrow : go forward
            Down arrow : go backward
            Left arrow : go left
            Right arrow : go right
            CTRL+C to quit
        """
        self.keyboard_controls={  #dictionary containing the key pressed abd value associated with it
                            '[A': 10, # up arrow fwd pitch
                            '[D': 30, # left arrow left roll
                            '[C': 40, # right arrow right roll
                            'w':50, # increase throttle
                            's':60, # decrease throttle
                            ' ': 70, # arm disarm
                            'r':80, # reset
                            't':90, # autopilot
                            'p':100,
                            '[B':110, # down arrow bkwd pitch
                            'n':120,
                            'q':130, # take off
                            'e':140, # land
                            'a':150, # left yaw
                            'd':160, # right yaw
                            '+' : 15,
                            '1' : 25,
                            '2' : 30,
                            '3' : 35,
                            '4' : 45,
                            # Windows arrow key 
                            'à': 42
                            # 'àH': 10, # up arrow fwd pitch (Windows)
                            # 'àK': 30, # left arrow left roll (Windows)
                            # 'àM': 40, # right arrow right roll (Windows)
                            # 'àP': 110 # down arrow bkwd pitch (Windows)
                            }

        self.win_arrowkey = False

        self.settings = self.saveTerminalSettings()  
        print(msg) 
        try:
            while(True):
                if(stat):
                    print("Roll :",self.get_roll(), "Pitch :",self.get_pitch(), "Yaw :",self.get_yaw(), "Battery :",self.get_battery())
                key = self.getKey(self.settings)
                if key in self.keyboard_controls.keys():
                    print("executed" , self.keyboard_controls[key] , "]]]")
                    self.indentify_key(self.keyboard_controls[key])

                else:
                    if(self.armed):
                        self.reset_speed()
                    print("Other key: ", key)
                    if (key == '\x03'):
                        print("Ctrl+C detected")
                        self.disarm() # Ctrl+C break
                        break

        except Exception as e:
            print(e)

        finally:
            print(key)
            self.restoreTerminalSettings(self.settings)
