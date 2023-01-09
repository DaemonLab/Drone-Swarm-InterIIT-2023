from pypluto.pluto import *

#import threading

import sys
from select import select
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

is_armed = False
msg = """
    Control Your Drone!
    ---------------------------
    spacebar : arm or disarm
    w : increase height
    s : decrease height
    q : take off
    e : land
    a : yaw left
    d : yaw right
    Up arrow : go forward
    Down arrow : go backward
    Left arrow : go left
    Right arrow : go right
    CTRL+C to quit
    """
keyboard_control={  #dictionary containing the key pressed abd value associated with it
                    '[A': 10, # up arrow fwd pitch
                    '[D': 30, # left arrow left roll
                    '[C': 40, # right arrow right roll
                    'w':50, # increase throttle
                    's':60, # decrease throttle
                    ' ': 70, # arm disarm
                    'r':80, # reset
                    't':90, # autopilot
                    'p':100,
                    '[B':110, # down arrow bkwd pitch
                    'n':120,
                    'q':130, # take off
                    'e':140, # land
                    'a':150, # left yaw
                    'd':160, # right yaw
                    '+' : 15,
                    '1' : 25,
                    '2' : 30,
                    '3' : 35,
                    '4' : 45}


def getKey(settings):
    """
    Function Name: getKey
    Input: None
    Output: keyboard charecter pressed
    Logic: Determine the keyboard key pressed
    Example call: getkey()
    """
    
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        if (key == '\x1b'): # \x1b is Escape key
            key = sys.stdin.read(2)
        sys.stdin.flush()
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    print(key)
    return key
    
def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def indentify_key(client,key_value):
    """
    Function to identify the key pressed and call
    the corresponding command function defined in movement.py
    and pluto.py
    """
    global is_armed 
    if key_value == 70:
        if is_armed:
            client.disarm()
            is_armed = not is_armed
        else:
            client.arm()
            is_armed = not is_armed

    elif key_value == 10:
        client.steer("forward",200) # forward

    elif key_value == 30:
        client.steer("left",200) # left

    elif key_value == 40:
        client.steer("right",200) # right

    elif key_value == 80:
        client.reset()

    elif key_value == 50:
        client.steer("up",400) # increase height

    elif key_value == 60:
        client.steer("down",20) # decrease_height

    elif key_value == 110:
        client.steer("backward",200) # backwards

    elif key_value == 130:
        client.takeoff()

    elif key_value == 140:
        client.land()

    elif key_value == 150:
        client.steer("anticlck",300) # yaw left

    elif key_value == 160:
        client.steer("clck",300) # yaw right

if __name__ == '__main__':
    settings = saveTerminalSettings()
    
    client = Drone()
    client.disarm()

    try:
        print(msg)
        while(True):
            key = getKey(settings)
            if key in keyboard_control.keys():
                print("executed" , keyboard_control[key] , "]]]")
                indentify_key(client,keyboard_control[key])

            else:
                client.steer("up",0)
                if (key == '\x03'):
                    client.disarm() # Ctrl+C break
                    break

    except Exception as e:
        print(e)

    finally:
        print(key)
        restoreTerminalSettings(settings)