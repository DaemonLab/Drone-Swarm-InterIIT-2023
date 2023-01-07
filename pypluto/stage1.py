# stage1.py
import time
import random
from multiprocessing import Process, Queue
from stage2 import Stage2



class Stage1:

  def stage1(self, queueS1, queueS2):
      print("stage1")
      lala = []
      lis = [1, 2, 3, 4, 5]
      for i in range(len(lis)):
          if not queueS2.empty():
              msg = queueS2.get()    # get msg from s2
              print("! ! ! stage1 RECEIVED from s2:", msg)
              lala = [6, 7, 8] # now that a msg was received, further msgs will be different
          time.sleep(1) # work
          random.shuffle(lis)
          queueS1.put(lis + lala)             
      queueS1.put('s1 is DONE')
      
      
s1= Stage1()
s2= Stage2()
# S1 to S2 communication
queueS1 = Queue()  # s1.stage1() writes to queueS1

# S2 to S1 communication
queueS2 = Queue()  # s2.stage2() writes to queueS2

# start s2 as another process
s2 = Process(target=s2.stage2, args=(queueS1, queueS2))
s2.daemon = True
s2.start()     # Launch the stage2 process
s1.stage1(queueS1, queueS2) # start sending stuff from s1 to s2 
s2.join() # wait till s2 daemon finishes

