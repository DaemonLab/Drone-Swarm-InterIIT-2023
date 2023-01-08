# Drone-Swarm

This Branch
- master starts these two files (  starts processes p1(associated with camera ) & p2( associated with actual control of drone1)

```
master
├── camerafile (marker.py sends continuous pose-data to pid file)
└── drone1 (drone1_pid.py continously gets data from marker & publishes data to drone using api functions)         
```
  
  To Do-
- Sending the actual calculated values from posefile( marker) to pidfile instead of current pseudo values( camera wasn't working)
( done now in SWARMY2)
