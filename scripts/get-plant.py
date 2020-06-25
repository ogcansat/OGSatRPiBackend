#!/usr/bin/env python3.7
import pandas as p
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import sys
import configparser

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

bpej = sys.argv[1]
bpej_v = bpej.split('.')

df = p.read_csv(config.get("Paths", "PlantTrainFileAI"), encoding="utf8")

x_train = df[["klimaticky_region","hlavni_pudni_jednotka","sklonitost_a_expozice","skeletovitost_a_hloubka_pudy"]]
y_train = df["rostlina_strom"]

#scaler = MinMaxScaler(feature_range=(0, 9))
#x_train = scaler.fit_transform(x_train)

ai_plant = KNeighborsClassifier()
ai_plant.fit(x_train, y_train)

plant = ai_plant.predict_proba([[bpej_v[0],bpej_v[1],bpej_v[2][0],bpej_v[2][1]]])[0]

pipe_plant = open(config.get("Paths", "PipePlant"), "w")
print(str(plant))
pipe_plant.write(str(plant))
pipe_plant.close()