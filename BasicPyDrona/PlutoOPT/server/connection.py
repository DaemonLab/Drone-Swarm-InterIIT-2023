import telnetlib

# DRONEIP = "192.168.4.1"
# DRONEPORT = "23"

class Connection():

    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        
    def connect(self):
        try:
            tn=telnetlib.Telnet(self.DRONEIP,self.DRONEPORT)
            print("\nPluto connected")
        except:
            print("\nCannot connect to pluto, please try again...")

    def disconnect(self):
        self.tn.close()
        print("\nPluto disconnected")

    def create_data_packet( self, cmd_list ):
        pass