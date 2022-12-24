"Entry "
from pypluto.pluto import Drone
from pypluto import *
import time

import sys
from select import select
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

"""
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
                    '[D': 30, # left arrow left pitch
                    '[C': 40, # right arrow right roll
                    'w':50, # increase throttle
                    's':60, # decrease throttle
                    ' ': 70, # arm disarm
                    'r':80, # 
                    't':90,
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

if __name__ == '__main__':
    settings = saveTerminalSettings()
    
    client = Drone()
    # client.arm()
    # time.sleep(2)
    # client.takeOff()
    # time.sleep(2)
    # client.forward()
    # time.sleep(2)
    # client.land()
    # client.disArm()
    try:
        while(1):
            key = getKey(settings)
            print("YO" , key , "YO", sep='')
            if key in keyboard_control.keys():
                print("executed" , keyboard_control[key] , "]]]")
                if (keyboard_control[key] == 70):
                    client.arm()
                    time.sleep(2)
            else:
                if (key == '\x03'): # Ctrl+C break
                    break

    except Exception as e:
        print(e)

    finally:
        print(key)
        restoreTerminalSettings(settings)
