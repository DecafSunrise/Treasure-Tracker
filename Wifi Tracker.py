"""
Treasure hunt wifi tracker
Script to run an adafruit feather to guide folks to a specified, squawking Wifi AP (to use as terminal guidance for a scavenger hunt)

Getting Circuit Python on the Feather: https://learn.adafruit.com/adafruit-esp32-s2-feather/overview
NeoPixel docs: https://learn.adafruit.com/adafruit-esp32-s2-feather/neopixel-led
Buzzer docs: https://learn.adafruit.com/using-piezo-buzzers-with-circuitpython-arduino/circuitpython
Multitasking: https://learn.adafruit.com/multi-tasking-with-circuitpython/all-together-now
"""

import board
import digitalio
import time
import pwmio
import wifi

import board
import neopixel

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

def buzz(note, lookup_rssi=-10):
    buzzer.duty_cycle = volume_glue[lookup_rssi]  # 32768 value is 50% duty cycle, a square wave.
    to_play = notes[note]
    buzzer.frequency = to_play - 300
    time.sleep(0.025)
    buzzer.frequency = to_play
    time.sleep(0.05)
    buzzer.frequency = to_play + 100
    time.sleep(0.1)
    buzzer.duty_cycle = 0
    time.sleep(0.1)

# Define a list of tones/music notes to play.
notes = {'C4': 262,
         'D4': 294,
         'E4': 330,
         'F4': 349,
         'G4': 392,
         'A4': 440,
         'B4': 494,
         'C5': 523,
         'D5': 587,
         'E5': 659,
         'F5': 698,
         'G5': 784,
         'A5': 880,
         'B5': 988,
         'C6': 1047,
         'D6': 1175,
         'E6': 1319,
         'F6': 1397,
         'G6': 1568,
         'A6': 1760,
         'B6': 1976}

note_glue = {-10: 'B6',
        -14: 'A6',
        -18: 'G6',
        -22: 'F6',
        -26: 'E6',
        -30: 'D6',
        -34: 'C6',
        -38: 'B5',
        -42: 'A5',
        -46: 'G5',
        -50: 'F5',
        -54: 'E5',
        -58: 'D5',
        -62: 'C5',
        -66: 'B4',
        -70: 'A4',
        -74: 'G4',
        -78: 'F4',
        -82: 'E4',
        -86: 'D4',
        -90: 'C4'}

volume_glue = {-10: 6993,
             -14: 6660,
             -18: 6327,
             -22: 5994,
             -26: 5661,
             -30: 5328,
             -34: 4995,
             -38: 4662,
             -42: 4329,
             -46: 3996,
             -50: 3663,
             -54: 3330,
             -58: 2997,
             -62: 2664,
             -66: 2331,
             -70: 1998,
             -74: 1665,
             -78: 1332,
             -82: 999,
             -86: 666,
             -90: 333}

# Set up a lookup table dict for RGB values
led_color_dict = make_color_dict()

for key in note_glue.keys():
    led_color_dict[key]['note'] = note_glue[key]

for key in volume_glue.keys():
    led_color_dict[key]['volume'] = volume_glue[key]

print(led_color_dict)

monitorlist = ['Network1', 'Network2']

# Neopixel; uses external adafruit lib
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Create piezo buzzer PWM output.
buzzer = pwmio.PWMOut(board.D5, variable_frequency=True)

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
        
        print(led_color_dict[lookup_rssi]['note'])
        
        # You could be smarter about this and just feed the RSSI
        buzz(led_color_dict[lookup_rssi]['note'], lookup_rssi)
        buzz(led_color_dict[lookup_rssi]['note'], lookup_rssi)
    
        ## If you wanna get fancy you could make this a carriage return situation
        print(f"Closest Network: {closest_net}")
        print(f"RSSI: {closest_net_rssi}")
    print("------\n")
    
    time.sleep(1)
