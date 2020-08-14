#!/usr/bin/env python3.7
import pandas as p
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import sys
import configparser
import csv
import random

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

bpej = sys.argv[1]
#bpej = "6.20.70"

bpej_v = bpej.split('.')
# df = p.DataFrame({"Bříza bělokorá (strom)": ["Pravděpodobnost: 80%"]})
# df.to_csv(config.get("Paths", "PipePlant"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")


df = p.read_csv(config.get("Paths", "PlantTrainFileAI"), sep=";",encoding="utf8")

codes = df[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]

mySet = p.DataFrame(columns = ["Rostlina", "Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"])

for i in range(len(df.index)):
    for j in range(5):
        plant = str(df.iloc[i,0]) + " " + str(df.iloc[i,1]) + " (" + str(df.iloc[i,2]) + ")"
        df2 = p.DataFrame([[plant, random.choice(str(codes.loc[i, "Klimatický region"]).split(',')),random.choice(str(codes.loc[i, "Hlavní půdní jednotka"]).split(',')),random.choice(str(codes.loc[i, "Sklonitost a expozice"]).split(',')),random.choice(str(codes.loc[i, "Skeletovitost a hloubka půdy"]).split(','))]], columns = ["Rostlina", "Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"])
        mySet= mySet.append(df2)



#x_train = df[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]


y_train = mySet[["Rostlina"]]
x_train = mySet[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]

#x_train.to_csv(config.get("Paths", "PipePlant"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")

#x_train = x_train[0][0].str.split(",", expand=True)

# #scaler = MinMaxScaler(feature_range=(0, 9))
# #x_train = scaler.fit_transform(x_train)

ai_plant = KNeighborsClassifier()
ai_plant.fit(x_train, y_train)

plant_proba = ai_plant.predict_proba([[bpej_v[0],bpej_v[1],bpej_v[2][0],bpej_v[2][1]]])[0]

pipe_plant = open(config.get("Paths", "PipePlant"), "w")

plant_line = ""
proba_line = ""

for x in range(len(df.index)):
    if (plant_proba[x] == 0):
        continue
    else:
        plant_line += str(df.iloc[x,0]) + " " + str(df.iloc[x,1]) + " (" + str(df.iloc[x,2]) + ")"
        proba_line += "Vhodnost: " + '{0:.0%}'.format(plant_proba[x])
        if (len(df.index) - 1) > x:
            plant_line += ";"
            proba_line += ";"

pipe_plant.write(plant_line)
pipe_plant.write("\n")
pipe_plant.write(proba_line)

pipe_plant.close()


print(str(plant_proba))

