#!/usr/bin/env python3.7
import pandas as p
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import sys
import configparser
import csv

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

#bpej = sys.argv[1]
bpej = "2.50.10"

bpej_v = bpej.split('.')
# df = p.DataFrame({"Bříza bělokorá (strom)": ["Pravděpodobnost: 80%"]})
# df.to_csv(config.get("Paths", "PipePlant"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")


df = p.read_csv(config.get("Paths", "PlantTrainFileAI"), sep=";",encoding="utf8")

codes = df[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]

mySet = p.DataFrame(columns = ["Rostlina", "Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"])

for i in range(len(df.index)):
    for j in range(5):
        plant = str(df.iloc[i,0]) + " " + str(df.iloc[i,1]) + " (" + str(df.iloc[i,2]) + ")"
        df2 = p.DataFrame([[plant, 2,4,5,6]], columns = ["Rostlina", "Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"])
        mySet= mySet.append(df2)


#x_train = df[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]


y_train = mySet[["Rostlina"]]
x_train = mySet[["Klimatický region","Hlavní půdní jednotka","Sklonitost a expozice","Skeletovitost a hloubka půdy"]]

#x_train = x_train[0][0].str.split(",", expand=True)

# #scaler = MinMaxScaler(feature_range=(0, 9))
# #x_train = scaler.fit_transform(x_train)

ai_plant = KNeighborsClassifier()
ai_plant.fit(x_train, y_train)

plant = ai_plant.predict_proba([[bpej_v[0],bpej_v[1],bpej_v[2][0],bpej_v[2][1]]])[0]

#plant = ai_plant.predict_proba([[bpej_v[0]]])[0]

pipe_plant = open(config.get("Paths", "PipePlant"), "w")
print(str(plant))
pipe_plant.write(str(plant))
pipe_plant.close()