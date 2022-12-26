import telnetlib


'''
const int PORT = 23;
const char* IP_ADDRESS = "192.168.4.1";
const int CAMERA_PORT = 9060;
const char* CAMERA_IP_ADDRESS = "192.168.0.1";
'''



class Connection():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        print("Connecting to Pluto......")
        
    def connect(self):
        try:
            self.tn = telnetlib.Telnet(self.DRONEIP, self.DRONEPORT)
            print("pluto connected")
            return self.tn
        except:
            print("Error While Connecting to Pluto")

    def disconnect(self):
        self.tn.close()
        print("Server connection closed")
