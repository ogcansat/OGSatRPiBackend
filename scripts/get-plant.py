#!/usr/bin/env python3.7
import pandas as p
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import sys

bpej = sys.argv[1]
bpej_v = bpej.split('.')

df = p.read_csv("/home/pi/Documents/OGSatProject/scripts/project4/BPEJ_20200203_3_edt_short2.csv", encoding="utf8")

x_train = df[["klimaticky_region","hlavni_pudni_jednotka","sklonitost_a_expozice","skeletovitost_a_hloubka_pudy"]]
y_train = df["rostlina_strom"]

#scaler = MinMaxScaler(feature_range=(0, 9))
#x_train = scaler.fit_transform(x_train)

ai_plant = KNeighborsClassifier()
ai_plant.fit(x_train, y_train)

plant = ai_plant.predict_proba([[bpej_v[0],bpej_v[1],bpej_v[2][0],bpej_v[2][1]]])[0]

pipe_plant = open("/home/pi/Documents/OGSatProject/scripts/project4/pipe_plant", "w")
pipe_plant.write(str(plant))
pipe_plant.close()