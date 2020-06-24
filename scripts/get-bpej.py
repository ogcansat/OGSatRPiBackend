#!/usr/bin/env python3.7

import shapely.geometry as geometry
import json
import sys


#Brno-venkov
#c_long = 16.432409
#c_lat = 49.144119

#Brno
#c_long = 16.651364
#c_lat=49.193057

#Žďár nad Sázavou
#c_long =16.147516
#c_lat = 49.599675

#Beskydy
#c_long = 18.531342
#c_lat = 49.539390

#Jeseníky - mimo
#c_long = 17.197241
#c_lat = 50.114442

c_long = float(0.000)
c_lat = float(0.000)

if len(sys.argv) == 3:
    c_long = float(sys.argv[1])
    c_lat = float(sys.argv[2])
elif len(sys.argv) == 2 and sys.argv[1] == "from_sat":
    data = open("/home/pi/Documents/OGSatProject/scripts/project4/pipe_data", "r")
    lines = data.readlines()
    if lines[0].split(',')[1] == "MessageID":
        c_long = float(lines[1].split(',')[7])
        c_lat = float(lines[1].split(',')[6])
    else:
        sys.exit()
else:
    sys.exit()


c_long_bpej = -68961* (180   - c_long) + 1.067*(10**7)
c_lat_bpej = -119992*(90 - c_lat) + 3.744*(10**6)
p_gps = geometry.Point(c_long, c_lat)
p_bpej = geometry.Point(c_long_bpej, c_lat_bpej)

#Start phase 1
print("***** Start Phase 1 *****\n")

print("Loading districts...")

#file with coordinates of czechia districts
dis_f = open("/home/pi/Documents/OGSatProject/scripts/project4/czechia_districts.json", "r", encoding="utf-8")
dis_data = json.load(dis_f)

districts = {}
for i in range(77):
    name = dis_data["features"][i]["properties"]["NAME_2"]
    region = dis_data["features"][i]["properties"]["NAME_1"]
    
    #directory containing files of czechia-districts containing BPEJ codes for district
    f = open("/home/pi/Documents/OGSatProject/scripts/project4/czechia-districts_corr/" + name + ".csv", "r", encoding="utf-8")

    if dis_data["features"][i]["geometry"]["type"] == "Polygon":
        if len(dis_data["features"][i]["geometry"]["coordinates"]) == 2:
           pol = geometry.Polygon(dis_data["features"][i]["geometry"]["coordinates"][0], [dis_data["features"][i]["geometry"]["coordinates"][1]])
        else:
            pol = geometry.Polygon(dis_data["features"][i]["geometry"]["coordinates"][0])
    elif dis_data["features"][i]["geometry"]["type"] == "MultiPolygon":
        pol = geometry.MultiPolygon(dis_data["features"][i]["geometry"]["coordinates"][0], dis_data["features"][i]["geometry"]["coordinates"][1])

    districts.update({name: [pol,f, region]})

print("Districts loaded.")

print("\n***** End Phase 1 *****")
#End phase 1

#Start phase 2
print("***** Start Phase 2 *****\n")

f_search = None
dis_now = "out of CZ"
region_now = "out of CZ"

for d in districts.items():
    if d[1][0].contains(p_gps):
        print("Point was founded at " + d[0] + " district.")
        f_search = d[1][1]
        dis_now = d[0]
        region_now = d[1][2]
        break

if f_search == None:
    f = open("/home/pi/Documents/OGSatProject/scripts/project4/pipe_bpej", "w")
    f.write("0.00.00" + "," + dis_now + "," + region_now)
    f.close()
    sys.exit()

print("\n***** End Phase 2 *****")
#End phase 2


#Start phase 3
print("***** Start Phase 3 *****\n")

i= 0
dis_min = -1
near_bpej = None
for row in f_search.readlines():
    i+=1
    values = str(row).split(';')

    arr = []

    for pol in values[2].split('&'):
        for in_out in str(pol).split('*'):
            for data in str(in_out).split('|'):
                if data != "":
                    data = data.split(',')
                    arr.insert(len(arr), [float(data[0]), float(data[1])])
            break
        break

    pol = geometry.Polygon(arr)

    if values[0] != "99":
        dis = p_bpej.distance(pol)
        if (dis < dis_min) or (dis_min == -1):
            dis_min = dis
            near_bpej = values[0]

    if pol.contains(p_bpej):
        print("BPEJ for your location: " + str(values[0]))
        break

print("Nearest BPEJ for your location: " + str(near_bpej))

f = open("/home/pi/Documents/OGSatProject/scripts/project4/pipe_bpej", "w")
f.write(near_bpej + "," + dis_now + "," + region_now)
f.close()



    #if i % 100 == 0:
    #    print("Row: " + str(i))


print("\n***** End Phase 3 *****")
#End phase 3