msg = "D"
class out_stream():
    
    #def __init__(self):
        #self.move_cmd = Move()
    
    def sendMsg(self, child_conn):
        global msg
        child_conn.send(str(msg))
        #child_conn.close()
        
    def arm(self):
        #print("Entered")
        global msg
        msg = "TO ARRRMMMSSSSS!!!!!!!!!"
        #print(msg)
        
    def disarm(self):
        self.sendMsg(self.move_cmd.arming(False))
        
