"Entry "
from pypluto.pluto import Drone
from pypluto import *
import time

#import threading

import sys
from select import select
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

msg = """
    Control Your Drone!
    ---------------------------
    Moving around:
    u    i    o
    j    k    l
    n    m    ,
    spacebar : arm or disarm
    w : increase height
    s : decrease height
    q : take off
    e : land
    a : yaw left
    d : yaw right
    t : auto pilot on/off
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

    #control_to_change_value=('u','o',',','z','c')


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

    # cmd = MsgType()
    if key_value == 70:
        # if(cmd.rcAUX4 == 1500):
        #     disarm()
        # else:
        client.arm()
    elif key_value == 10:
        client.forward()
    elif key_value == 30:
        client.left()
    elif key_value == 40:
        client.right()
    elif key_value == 80:
        client.reset()
    # elif key_value == 90:
    #     if(cmd.isAutoPilotOn == 1):
    #         cmd.isAutoPilotOn = 0
    #     else:
    #         cmd.isAutoPilotOn = 1
    elif key_value == 50:
        client.increase_height()
    elif key_value == 60:
        client.decrease_height()
    elif key_value == 110:
        client.backward()
    elif key_value == 130:
        client.takeOff()
    elif key_value == 140:
        client.land()
    elif key_value == 150:
        client.anticlockwise()
    elif key_value == 160:
        client.clockwise()

if __name__ == '__main__':
    settings = saveTerminalSettings()
    
    client = Drone()

    try:
        print(msg)
        while(1):
            key = getKey(settings)
            print("YO" , key , "YO", sep='')
            if key in keyboard_control.keys():
                print("executed" , keyboard_control[key] , "]]]")
                indentify_key(client,keyboard_control[key])
                # if (keyboard_control[key] == 70):
                #     client.arm()
                    #time.sleep(2)

            else:
                if (key == '\x03'): # Ctrl+C break
                    break
            client.getIMU()

    except Exception as e:
        print(e)

    finally:
        print(key)
        restoreTerminalSettings(settings)
