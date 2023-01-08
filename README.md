# Drone-Swarm

This Branch
- master starts these two files (  starts processes p1(associated with camera ) & p2( associated with actual control of drone1)
-                        |
-             ___________|_________________________________
-             |                                       |
-             camerafile                            pidfile
-             (marker.py)                         (drone1_pid)
-     (send conti pose-data to pid file )       ( continously gets data from marker & publishes data to drone using api functions)


          
  
  
  To Do-
- Sending the actual calculated values from posefile( marker) to pidfile instead of current pseudo values( camera wasn't working)
