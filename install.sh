#!/bin/bash

# necessary to do this since I cannot manage access to my Documents folder since Catalina
cp ./discipline.py ~/.discipline.py

# remember to change the username and the wifi SSID(s)!
cp ./examples/local.discipline.morning.plist /Library/LaunchDaemons/
cp ./examples/local.discipline.noon.plist /Library/LaunchDaemons/
cp ./examples/local.discipline.sleep.plist /Library/LaunchDaemons/
