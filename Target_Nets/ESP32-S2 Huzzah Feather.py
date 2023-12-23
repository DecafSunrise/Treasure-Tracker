"""
Setting up a simple "rabbit" network.

This code is for the Adafruit "Huzzah Feather" ESP32-S2, so it runs circuitpython. 
"""

import wifi
from time import sleep
import board
import neopixel

## Wifi
node_name = "Node-Whiskey"
wifi.radio.start_ap(ssid=node_name, password="")

## NeoPixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.fill((0, 255, 0))
max_bright = 0.1
min_bright = 0
num_steps = 200
step_size = max_bright/num_steps

## Run a loop so the board keeps serving the network
while True:
    while pixel.brightness < max_bright:        
        pixel.brightness += step_size
        sleep(0.01)
    while pixel.brightness > min_bright:
        pixel.brightness -= step_size
        sleep(0.01)
