#!/usr/bin/env python

import serial
import os
import time
import re
import subprocess as sub
import sys
import traceback
import ConfigParser
import pandas as p
import io

def write_data(columns, data, delimiter=':'):
    i = 0
    for column in columns:
        dev.write(column + delimiter + data[i] + "\n")
        i+=1

# Start of Initialization
config = ConfigParser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

dev = None
conn = False
data_sending = False
data_sat = False

pipe_data = config.get("Paths", "PipeData")
last_data = open(pipe_data, "r").read()

# End of Initialization


# Start of endless loop
while True:

    try: 
        conn = True if os.path.exists("/dev/rfcomm0") else False

        if dev == None and conn:
            dev = serial.Serial("/dev/rfcomm0")
            print("Communication established.")

            

        if conn and (dev != None):                           

            received = None

            if dev.in_waiting > 0:

                received = dev.read(dev.in_waiting)
                received = re.sub("\r\n", "", received)
                print("Received message: " + received) 

                if received == "shutdown":  
                    print("Shutting down...")
                    time.sleep(1)
                    sub.call(["sudo", "shutdown", "now"])
                elif received == "reboot":
                    print("Rebooting...")
                    time.sleep(1)
                    sub.call(["sudo", "reboot", "now"])
                elif received.startswith("dataON"):   
                    data_dev = received.split(' ')[1]    
                    if data_dev == "sat":
                        data_sat = True
                        data_sending = True
                    elif data_dev == "bs":
                        data_sat = False
                        data_sending = True
                elif received == "dataOFF":
                    data_sending = False
                elif received == "restartOG":
                    sub.call(["sudo", "systemctl", "restart", "bs-monitor.service"])   
                elif received.startswith("get_bpej"):
                    pipe_bpej = open(config.get("Paths", "PipeBPEJ"), "r")

                    #coordinates = received.split('\xc2\xa0')  
                    coordinates = received.split(' ')  

                    if len(coordinates) == 3:
                        sub.call(["python3.7", config.get("Paths", "BPEJscript"), coordinates[1], coordinates[2]])
                    elif len(coordinates) == 2:
                        sub.call(["python3.7", config.get("Paths", "BPEJscript"), coordinates[1]])
                    time.sleep(1)

                    dev.write(pipe_bpej.readline())
               
                elif received.startswith("get_plant"):
                    pipe_plant = open(config.get("Paths", "PipePlant"), "r")

                    bpej_code = received.split(' ')[1] 

                    print("BPEJ evaluating for plant...")

                    sub.call(["python3.7", config.get("Paths", "PlantScript"), bpej_code])
                    time.sleep(1)

                    dev.write(pipe_plant.readline())
                elif received.startswith("getBPEJ"):
                    argsBPEJ = received.split(' ')

                    codeBPEJ = argsBPEJ[1]

                    sub.call(["python3.7", config.get("Paths", "ScriptInfoBPEJ"), codeBPEJ])

                    print("Sending BPEJ info about a code " + codeBPEJ + " to the mobile...")

                    pipe_infoBPEJ = open(config.get("Paths", "PipeBPEJinfo"), "r")
                    dev.write(pipe_infoBPEJ.read())
                elif received.startswith("getPlants"):
                    plants = open(config.get("Paths","FilesBPEJ") + "/Rostliny.csv", "r").read()
                    dev.write(plants)
                    
                    

                
            if data_sending:
                
                data_file = open(pipe_data, "r")
                now_data = data_file.read()

                if last_data != now_data:  
                    if now_data.split(',')[1] == "MessageID" and data_sat:  
                        lines = now_data.splitlines()
                        write_data(lines[0].replace('\n', '').split(',')[1:], lines[1].split(',')[1:])                  

                        last_data = now_data
                    elif now_data.split(',')[1] == "Light" and not(data_sat):
                        lines = now_data.splitlines()
                        write_data(lines[0].replace('\n', '').split(',')[1:], lines[1].split(',')[1:])

                        last_data = now_data

            time.sleep(0.05)

    except Exception:                 
        print("Communication interrupted.")   
        traceback.print_exc()      
        if dev != None:
            dev.close()
            dev = None
        conn = False
        data_sending = False      
    
    time.sleep(0.5)

#End of endless loop    
