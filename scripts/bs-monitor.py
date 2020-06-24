#!/usr/bin/env python

import serial
import os
import re
import sys
import pandas as p
import datetime
import traceback
import time
import subprocess as sub
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

def change_char(s, p, r):
    return s[:p]+r

print("Initialization...")

date_now = datetime.datetime.now()
path = "/dev/ttyACM"
data_file_prefix = config.get("Paths", "DataFolder") + "/data_%s-%s-%sa" % (date_now.year, date_now.month, date_now.day)
pipe_data = config.get("Paths", "PipeData") 
pipe_bpej = open(config.get("Paths", "PipeBPEJ"), "r")
row_sat = 1
row_bs = 1

data_sat_file = ""
data_bs_file = ""


for i in range(10):
    if os.path.exists(path + str(i)):
        path = path + str(i)
        print("Arduino was found on port: %s" % path)
        break
else:
    print("Arduino was't found.")
    sys.exit()

arduino = serial.Serial(
        port=path,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        write_timeout=0.5,
        timeout=300
        )

for i in range(98,123):
    if os.path.exists(data_file_prefix + "-sat.csv") or os.path.exists(data_file_prefix + "-bs.csv"):
        data_file_prefix = change_char(data_file_prefix, -1, chr(i))
    else:
        print("The data file prefix: %s" % data_file_prefix)
        data_sat_file = data_file_prefix + "-sat.csv"
        data_bs_file = data_file_prefix + "-bs.csv"
        break


columns_order_sat = ["MessageID","Temperature", "Humidity", "Altitude", "Pressure", "Latitude", "Longitude","Hour", "Minute", "Second", "Day", "Month", "Year"]
columns_order_bs = ["Light", "Temperature", "Humidity", "Pressure", "Altitude", "SoilHum", "Hour", "Minute", "Second", "Day", "Month", "Year"]
template_sat = p.DataFrame([], columns=columns_order_sat)
template_sat.to_csv(data_sat_file)

template_bs = p.DataFrame([], columns=columns_order_bs)
template_bs.to_csv(data_bs_file)

#longitude = 16.432409
#latitude = 49.144119
#last_lat = 0.0
#last_long = 0.0
#last_bpej = ""

#bpej_evaluation = None


while True:
       
    try:
    
        print("-----------------------------------------")

        print("Receiving data from arduino...")
        received = arduino.readline()
    
        print("Data processing...")
        received = re.sub("\\r\\n", "", received)
        data = re.split(";", received)

        date_now = datetime.datetime.now()
        if data[0] == "SATELLITE":    
            print("Processing new satellite data...")
            df_data = p.DataFrame({"MessageID": [data[1]],"Temperature": [data[2]], "Humidity": [data[3]], "Altitude": [data[4]], "Pressure": [data[5]], "Latitude": [data[6]], "Longitude": [data[7]],
            "Hour": [date_now.hour], "Minute": [date_now.minute], "Second": [date_now.second], "Day": [date_now.day], "Month": [date_now.month], "Year": [date_now.year]}, 
            columns=columns_order_sat, index=[row_sat])
            #longitude = float(data[7])
            #latitude = float(data[6])
            df_data.to_csv(data_sat_file, mode="a", header=False)
            df_data.to_csv(pipe_data)     
            print("New satellite data:")
            print(df_data)
            row_sat+=1
        elif data[0] == "BASE-STATION":
            print("Processing new base-station data...")
            df_data = p.DataFrame({"Light": [data[1]], "Temperature": [data[2]], "Humidity": [data[3]], "Pressure": [data[4]], "Altitude": [data[5]], "SoilHum": [data[6]],
            "Hour": [date_now.hour], "Minute": [date_now.minute], "Second": [date_now.second], "Day": [date_now.day], "Month": [date_now.month], "Year": [date_now.year]}, 
            columns=columns_order_bs, index=[row_bs])
            df_data.to_csv(data_bs_file, mode="a", header=False)
            df_data.to_csv(pipe_data)     
            print("New base-station data:")
            print(df_data)  
            row_bs+=1 

        time.sleep(0.05)         

        
    except Exception:
        print("Connection with Base Station interrupted.")
        traceback.print_exc()
        sys.exit()

