"""
Creating a "fox" for foxhunting.

This code is for the M5StickC.

Web IDE for flashing: https://flow.m5stack.com/
"""

from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x000000)

T1 = M5Title(title="Tango", x=20, fgcolor=0xffffff, bgcolor=0x000000)

ssid = 'Node-Tango'
password = ''

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
