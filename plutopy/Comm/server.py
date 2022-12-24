import telnetlib


class Connection():
    def __init__(self, DroneIP="192.168.4.1", DronePort="23"):
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort

    def connect(self):
        try:
            self.tn = telnetlib.Telnet(self.DRONEIP, self.DRONEPORT)
            return self.tn
        except:
            print("Error While Connecting the Drone System.")

    def disconnect(self):
        self.tn.close()
        print("Server connection closed")