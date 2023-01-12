## Commands

### Initialisation
Initialising drone object with ```Drone IP``` and ```Port``` as arguements. If nothing is given as arguement, the default values defined in ```pluto.py``` are used.
```python
client = Drone("192.168.4.1","23")
```

### Arming and Disarming the drone
For arming and disarming the drone, use the following functions
```python
client.arm() # arm the drone
time.sleep(5)
```
```python
client.disarm() # disarm the drone
time.sleep(5)
```
Note: After **Arm** and **Disarm** some delay is important

### Takeoff and Landing
```python
client.takeoff() # take off
client.land() # land
```

### Flips

Currently, only one type of flip is supported in the API (backflips). Other types of flips (frontflips, rightflips and leftflips) will be implemented soon.
```python
client.backflip()
```

### Steering the drone in a particular direction
Use the following function to steer the drone in a particular direction
```python
client.steer("up", 400)
```
The first argument is the direction of steer, and it can take the following values (case-sensitive)
```python
direction = ["forward", "backward", "left", "right", "up", "down"]
```
The second argument specifies the magnitude over which the drone steers. If nothing is specified by user, the default value of 100 is used.
```
-600 < magnitude < 600
```
The final values, which the drone receives is 1500+Magnitude
### Set manual values for steering
One can also use the ```set_steer()``` function to manually set the values of drone ```roll, pitch, throttle, yaw``` values.

```python
client.set_steer([100, 100, 0, 50])
```

The argument sent is an array, magnitude, which has the following format
```python
magnitude = [roll, pitch, throttle, yaw]
```

### Setting Trim
To balance the drift in drone at central values of ```Roll, Pitch,Throttle, Yaw```, the trim function
```python
client.trim(5,-5,0,0)
```
The argument format is
```
(roll, pitch, throttle, yaw)
```
The sign of values should be opposite to which the drift is observed.<br>
For Roll: right hand side is positive<br>
For Pitch: forward positive<br>
For Throttle: upwards is positive<br>
For Yaw: Clockwise positive
