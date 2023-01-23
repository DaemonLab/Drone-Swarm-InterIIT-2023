
<div id="top"></div>

# Drone Swarm Python
API for controlling The Pluto 1.2 nano drone

#add a real  gif/photo of our drone here

[![](https://img.shields.io/badge/License-GPLv3-blue.svg)]()

<!-- TABLE OF CONTENTS (ADD ONCE SUBTOPICS START COMING TOGETHER)-->


## Index 
 
 

 1. <p><a href="#ProjD">Project Description</a></p>
 2. <p><a href="#RepoS">Repository Structure</a></p>
 3. <p><a href="#TechS">Tech Stack</a></p>
 4. <p><a href="#GetSL">Getting Started ( Linux / Windows) </a></p>
 5. <p><a href="#Usg">Usage</a></p>
	
	  a. Pre-Programmed Execution
	 b. Camera Feedback Execution
	 c. Keyboard Control
	 d. Manually stopping (killing) the drone

6. <p><a href="#ProjD">Demo</a></p>


 

<!-- PROJECT DESCRIPTION -->
<div id="ProjD"></div>

## 1. Project Description 

*Task 1*: 
Develop a Python wrapper for India's one and only number-one-selling educational nano drone, The Pluto.

*Task 2*: 
Hovering a pluto drone on a particular height using ArUco Tag. 
Set a web camera (which is not included in the kit) on the ceiling.
- A. Get a pose estimation of the drone using ArUco tag on the drone.
- B. Add PID to the script for controlling the droneC
- C. Hover the drone in one position.
- D. Move the drone in rectangular motion (1 x 2 meter)

*Task 3*: 
Pluto Swarming (A second drone will be provided - both the drones should fly
at the same time)
A. Generate one more ArUco tag and place it on the second drone.
B. Initially, Drone2 will be at position0, and drone1 will be at position1. Write
commands to move Drone1 from position1 to position2. When Drone1 reaches
position2, drone2 should follow drone1 and reach position1 automatically.
C. Same way, create a rectangle motion. (1 x 2 meter)
D. Record a video and make the final submission similarly as the previous one.


<div id="RepoS"></div>


## Repository structure
<pre>
├─docs
│    │  functions.md
│    └─keyboard_control.md
│  
├─pypluto
│    ├─pypluto
│    │   ├─Camera
│    │   |   | cam_configs.py
│    │   |   └─marker.py
│    │   |
│    │   ├─Control
│    │   |   └─ PIDmain.py
│    │   | 
│    │   |  __init__.py
│    │   |  drone.py
│    │   └─ enforce.py
│    │  
│    │   kill.py
│    │   main.py
│    │   master.py
│    └─  setup.py???
│    
├─PrimusV4-Pluto_1_2-1.hex
|
├─Tasks
│    │  Task1.md
│    │  Task2.md
│    └─ Task3.md
│
└─requirements.txt

</pre>

<div id="TechS"></div>

## 3. Tech Stack 

- python>=3.7
- numpy==1.17.4
- opencv_contrib_python==4.6.0.66
- setuptools==45.2.0
- matplotlib==3.1.2


<div id="GetSL"></div>

## 4. Getting Started - Linux

### Prerequisites

<!-- *Put setup instructions here.* -->

The API is tested with the ```PrimusV4-Pluto_1_2-1.hex``` firmware installed on Pluto Drone.

If ```pip3``` is not installed, install it using the following command in Terminal

```shell
$ sudo apt update
$ sudo apt install python3-pip
``` 

##### Using a Python environment is recommended considering the dependencies
```shell
$ pip install virtualenv
```
Now check your installation
```
$ virtualenv --version
```
Create a virtual environment now inside an appropriate folder,
this in for specific python version
```
$ virtualenv -p /usr/bin/python3 Drone_Env
```
After this command, a folder named  **Drone_Env**  will be created. 

Now at last we just need to activate it, using command
```
$ source Drone_Env/bin/activate
```
Now you are in a Drone's Python virtual environment

#check below cmds

```
$ git clone https://github.com//Drone-Swarm.git  #add appropriate
$ cd Drone-Swarm
$ python3 install setup.py
$ pip3 install -e .

```

You can deactivate environment using
```
$ deactivate 
```



<div id="GetSW"></div>

## Getting Started - **Windows**
Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) using cmd prompt
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
To install run the following command using cmd prompt
```
python /path/to/get-pip.py
```
Install the External Dependencies using the following command 
```
pip install -r requirements.txt
```
<div id="Usg"></div>

### 5. Usage

#### a. Pre-Programmed Execution
<!-- *Explain API cmds here.... might need a more detailed version like (make another section for structure)* -->

Use the ```main.py``` template file for pre-programming the drone movement( without using any external camera) .<br> 

Following is a sample program.
note: you might need to change the trim values depending on your drone.
```python
from pypluto import pluto

if __name__ == '__main__':
	#initializing the drone
	drone=pluto()
	drone.connect()
	drone.disarm()
	
	#drone plan execution
	drone.trim(-2,2,0,0)
	drone.takeoff()
	drone.throttle_speed(0,3)
	
	#closing the execution
	drone.land()
	drone.disarm()

```

For detailed explanation of use of various movement functions, refer to [functions.md](https://github.com//Drone-Swarm/blob/main/docs/functions.md) <br>

#### b. Camera Feedback Execution

Instructions for controlling the drone using camera setup can be found here-
[camera_pid.md](https://github.com//Drone-Swarm/blob/main/docs/camera_pid.md)


#### c. Keyboard Control

User can also control the drone from keyboard by running the ```keyboard.py``` file in terminal/command prompt. 
Instructions for control via keyboard can be found in [keyboard_control.md](https://github.com//Drone-Swarm/blob/main/docs/keyboard_control.md)


### d. Manually stopping (killing) the drone

Sometimes, it may happen that the python program using the API may end without deactivating (landing and/or disarming) the drone, and the drone may stay on. In that case, one can run the ```kill.py``` script, which will send the required commands to properly deactivate the drone. 

<div id="Demo"></div>

## Demo

Link to Drive : 

<p align="right">(<a href="#top">back to top</a>)</p>

<div id="RoadM"></div>
