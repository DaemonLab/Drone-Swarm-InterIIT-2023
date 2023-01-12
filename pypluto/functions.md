### Arming and Disarming the drone

For arming and disarming the drone, use the following functions
```python
client.arm() # arm the drone
client.disarm() # disarm the drone
```

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
The first argument is the direction of steer, and it can take the following values
```python
direction = ["forward", "backward", "left", "right", "up", "down"]
```
The second argument specifies the magnitude over which the drone steers
```
-600 < magnitude < 600
```

### Set manual values for steering
One can also use the set_steer() function to manually set the values of drone roll (sideways motion), pitch (forward and backward motion), throttle (upward and downward motion), and yaw (left and right steering motion)

```python
client.set_steer([100, 100, 0, 50])
```

The argument sent is an array, magnitude, which has the following format
```python
magnitude = [roll, pitch, throttle, yaw]
```