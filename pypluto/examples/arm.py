from pypluto import *
import time

t0 = time.time()

#print(time.time()-t0)
client = Drone()

print("Arm")
client.arm()
time.sleep(2)

print("Forward")
client.forward()
time.sleep(4)

print("Backward")
client.backward()
time.sleep(4)

print("Disarm")
client.disArm()
