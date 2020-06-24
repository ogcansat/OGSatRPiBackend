#!/usr/bin/env python

import subprocess as sub
import time

while (True):
    print("Syncing...")
    sub.call(["rclone", "sync", "/home/pi/Documents/OGSatProject/data", "OGDrive:data/"])
    print("Waiting...")
    time.sleep(300)
