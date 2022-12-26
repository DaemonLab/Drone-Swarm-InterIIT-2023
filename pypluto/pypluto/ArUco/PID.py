import numpy as np

class State:

    # to be tuned
    KP = 1.0
    KI = 0
    KD = 0

    def __init__(self):
        self.currentX = 0.0
        self.desiredX = 0.0  
        self.previousErr = 0.0
        self.integralErr = 0.0              
    
    def PIDcontrol(self, dt):

        Err = self.desiredX - self.currentX
        command = self.KP*Err + self.KD*(Err-self.previousErr)/dt + self.KI*self.integralErr

        self.previousErr = Err
        self.integralErr += Err*dt

        return command





        


