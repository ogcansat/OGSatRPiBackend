#!/usr/bin/env python

import subprocess as sub
import time
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

while (True):
    print("Syncing...")
    sub.call(["rclone", "sync", config.get("Paths", "DataFolder"), "OGDrive:data/"])
    print("Waiting...")
    time.sleep(300)
