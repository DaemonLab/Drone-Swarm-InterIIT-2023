<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![](https://img.shields.io/github/issues-pr-raw/DaemonLab/Drone-Swarm?color=important&style=for-the-badge)](https://github.com/DaemonLab/Drone-Swarm/pulls)

# Drone Swarm Python
This repository is being written for the Inter IIT Tech Meet 11.0 by the students of IIT Indore.

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

First, import the API at the top of your file
```python
from pypluto.pluto import *
```
Then, create a Drone object to be used for controlling the drone
```python
client = Drone()
```
This object uses the default IP address (192.168.4.1) and port (23) to connect to the drone. If another IP address or port is to be used, specify it in the constructor
```python
client = Drone("192.168.17.44","23")
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Usage
<!-- *Explain API cmds here.... might need a more detailed version like (make another section for structure)* -->

#### Arming and Disarming the drone

For arming and disarming the drone, use the following functions
```python
client.arm() # arm the drone
client.disarm() # disarm the drone
```

#### Takeoff and Landing

```python
client.takeoff() # take off
client.land() # land
```

#### Flips

Currently, only one type of flip is supported in the API (backflips). Other types of flips (frontflips, rightflips and leftflips) will be implemented soon.
```python
client.backflip()
```

#### Steering the drone in a particular direction
Use the following function to steer the drone in a particular direction
```python
client.steer("up", 400)
```
The first argument is the direction of steer, and it can take the following values
```python
direction = ["forward", "backward", "left", "right", "up", "down"]
```
The second argument specifies the magnitude over which the drone steers
```
-600 < magnitude < 600
```

#### Set manual values for steering
One can also use the set_steer() function to manually set the values of drone roll (sideways motion), pitch (forward and backward motion), throttle (upward and downward motion), and yaw (left and right steering motion)

```python
client.set_steer([100, 100, 0, 50])
```

The argument sent is an array, magnitude, which has the following format
```python
magnitude = [roll, pitch, throttle, yaw]
```

<!-- NOTE: These explanationa have been set according to my understanding of the drone code -->
<!-- Feel free to modify them if inaccurate -->

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
