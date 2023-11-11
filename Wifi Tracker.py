"""
Treasure hunt wifi tracker
Script to run an adafruit feather to guide folks to a specified, squawking Wifi AP (to use as terminal guidance for a scavenger hunt)

Getting Circuit Python on the Feather: https://learn.adafruit.com/adafruit-esp32-s2-feather/overview
NeoPixel docs: https://learn.adafruit.com/adafruit-esp32-s2-feather/neopixel-led
Buzzer docs: https://learn.adafruit.com/using-piezo-buzzers-with-circuitpython-arduino/circuitpython
"""

import board
import digitalio
import time

import wifi

import board
import neopixel

# Neopixel; uses external adafruit lib
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

## This is the built-in red LED/Power indicator
#led = digitalio.DigitalInOut(board.LED)
#led.direction = digitalio.Direction.OUTPUT

#while True:
#    led.value = True
#    time.sleep(3)
#    led.value = False
#    time.sleep(0.5)

def print_network_stats(network):
    """Utility function to quickly print network stats"""
    print(f"SSID: {network.ssid}")
    print(f"BSSID: {network.bssid}")
    print(f"Channel: {network.channel}")
    print(f"RSSI: {network.rssi}\n")

def make_color_dict():
    led_color_dict = {}
    color1 = 0
    color2 = 255
    for i in range(-10, -93, -4):
        led_color_dict[i] = {"red":int(color1), "green":int(color2)}
        color1 += 12.75
        color2 -= 12.75
        
    return led_color_dict

# Set up a lookup table dict for RGB values
led_color_dict = make_color_dict()

monitorlist = ['Network1', 'Network2']

while True:
    current_nets = {}
    for network in wifi.radio.start_scanning_networks():
        if network.ssid in monitorlist:
            current_nets[network.ssid] = network.rssi
#            print_network_stats(network)
#    print("----\n")
    wifi.radio.stop_scanning_networks()
    
    if len(current_nets)==0:
        # No networks in range
        pixel.fill((0, 0, 0))
        ## If you wanna get fancy you could make this a carriage return situation
        print(f"No network in range")
        
    else:
        # Network in range, turn on LED
        closest_net = max(current_nets, key=current_nets.get)
        closest_net_rssi = max(current_nets.values())
        lookup_rssi = min(led_color_dict.keys(), key=lambda key: abs(key - closest_net_rssi))
    
        current_red = led_color_dict[lookup_rssi]['red']
        current_green = led_color_dict[lookup_rssi]['green']    
        pixel.fill((current_red, current_green, 0))
    
        ## If you wanna get fancy you could make this a carriage return situation
        print(f"Closest Network: {closest_net}")
        print(f"RSSI: {closest_net_rssi}")
    print("------\n")
    
    time.sleep(1)
