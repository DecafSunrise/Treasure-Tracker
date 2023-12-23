"""
Setting up a simple "rabbit" network.
"""

import wifi

node_name = "<Your name here>"

wifi.radio.start_ap(ssid=node_name, password="")
