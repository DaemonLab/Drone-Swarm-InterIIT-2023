

-----------------------------Task 1 ;----------------------------------------
Check MSP and socket communication for Pluto.

A. Check the existing communication method used to communicate with Pluto.
status:
Current using telnet with MSP packets
(Pluto Communication MSP packets[2])

B. Creating a Python wrapper to control the drone movements. (Eg. Pitch forward, Roll
left, take off - Land, etc.)
flip cmds not working currently

C. Fly the drone using a Python wrapper (from a Linux Machine/Windows PC)


-----------------------------Task 2---------------------------------------
Hovering a pluto drone on a particular height using ArUco Tag. 

A. Generate the ArUco tag and place it on the drone. -------  done
B. Using ArUco tag, get a pose estimation of the drone.-----
C. Add PID to the script for controlling the drone
D. Hover the drone in one position.
E. Move the drone in rectangular motion (1 x 2 meter)
F. Record a video and send the code and video in the zip file to the sponsors.


-------------------------------Task 3----------------------------------------------- 
Pluto Swarming (A second drone will be provided - both the drones should fly
at the same time)
A. Generate one more ArUco tag and place it on the second drone.
B. Initially, Drone2 will be at position0, and drone1 will be at position1. Write
commands to move Drone1 from position1 to position2. 
When Drone1 reaches
position2, drone2 should follow drone1 and reach position1 automatically.

Strategy1  :  (credit : Kshitij B.)
get drone 1 at pt1 and then move drone2 wrt to drone1's current loc. 
( diagonal dist will be the error) but one line will be line of constriaint and other line of movement

