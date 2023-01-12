<div id="top"></div>

[![Issues][issues-shield]][issues-url]

# Drone Swarm Python
API for controlling The Pluto 1.2 nano drone

[![](https://img.shields.io/badge/License-GPLv3-blue.svg)]()

<!-- TABLE OF CONTENTS (ADD ONCE SUBTOPICS START COMING TOGETHER)-->


<!-- PROJECT DESCRIPTION -->

## Project Description 

*Task 1*: Develop a Python wrapper for India's one and only number-one-selling educational nano drone, The Pluto.

*Task 2*: Hovering a pluto drone on a particular height using ArUco Tag. Set a web camera (which is not included in the kit) on the ceiling.

*Task 3*: Pluto Swarming (A second drone will be provided - both the drones should fly at the same time)

## Getting Started

### Prerequisites

<!-- *Put setup instructions here.* -->

The API is tested with the ```PrimusV4-Pluto_1_2-1.hex``` firmware installed on Pluto Drone.

If ```pip3``` is not installed, install it using the following command on linux
```shell
$ sudo apt update
$ sudo apt install python3-pip
``` 
and for Windows
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


<p align="right">(<a href="#top">back to top</a>)</p>

### Usage
<!-- *Explain API cmds here.... might need a more detailed version like (make another section for structure)* -->

Use the ```main.py``` template file for programming the drone movement.<br> 
or refer to the following sample program.
```python
from pypluto.pluto import *

if __name__ == '__main__':
    client = Drone()
    
    client.disarm()
    time.sleep(5)
    
    client.arm()
    time.sleep(5)
    
    client.trim(50, -50, 0, 0)
    client.steer("up",400)
    time.sleep(4)
    
    client.land()
    time.sleep(4)
    
    client.disarm()
```

For detailed explanation on use of various movement functions refer to [functions.md](https://github.com/DaemonLab/Drone-Swarm/blob/main/pypluto/functions.md)

### Manually stopping (killing) the drone

Sometimes, it may happen that the python program using the API may end without deactivating (landing and/or disarming) the drone, and the drone may stay on. In that case, one can run the ```kill.py``` script, which will send the required commands to properly deactivate the drone. 

## Roadmap

### Finalized
- [x] Basic Control Commands
- [x] Sending commands continously with threading
- [x] Keyboard Control
- [x] ArUco Detection
- [x] Multiple Drones
- [ ] PID balancing with ArUco
- [ ] Take sensor data for height


<div id="ideas"></div>

### Ideas

- [ ] Modes and other flips
- [ ] Amphibian support

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact Us

Members :  

[contributors-shield]: https://img.shields.io/github/contributors/DaemonLab/Drone-Swarm?color=informational&style=for-the-badge
[contributors-url]: https://github.com/DaemonLab/Drone-Swarm/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DaemonLab/Drone-Swarm?color=blueviolet&style=for-the-badge
[forks-url]: https://github.com/DaemonLab/Drone-Swarm/fork
[stars-shield]: https://img.shields.io/github/stars/DaemonLab/Drone-Swarm?color=yellow&style=for-the-badge
[stars-url]: https://github.com/DaemonLab/Drone-Swarm/stargazers
[issues-shield]: https://img.shields.io/github/issues-raw/DaemonLab/Drone-Swarm?color=%23FF0000&style=for-the-badge
[issues-url]: https://github.com/DaemonLab/Drone-Swarm/issues
