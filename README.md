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

The API is tested with the ```PrimusV4-Pluto_1_2-1.hex``` firmware installed on Pluto Drone.

If ```pip``` is not installed, install it using the following command ```..``` <br>

Install the External Dependencies using the following command ```pip install -r requirements.txt```


<p align="right">(<a href="#top">back to top</a>)</p>

### Usage
<!-- *Explain API cmds here.... might need a more detailed version like (make another section for structure)* -->




## Manually stopping (killing) the drone

Sometimes, it may happen that the python program using the API may end without deactivating (landing and/or disarming) the drone, and the drone may stay on. In that case, one can run the **kill.py** script, which will send the required commands to properly deactivate the drone. 

Modify line 6 in the file as per the constructor you are using (if your IP address and port is not the default, as mentioned above in *'Prerequisites'* ).

```python
    client = Drone()
```

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
