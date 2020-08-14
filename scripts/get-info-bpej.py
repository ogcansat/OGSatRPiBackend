#!/usr/bin/env python3.7
import pandas
import configparser
import sys
import subprocess

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

files = config.get("Paths", "FilesBPEJ")

codeBPEJ = sys.argv[1]
typeBPEJ = sys.argv[2]

if typeBPEJ == "plants":
    subprocess.call(["python3.7", config.get("Paths", "PlantScript"), codeBPEJ])
    df = pandas.read_csv(config.get("Paths", "PipePlant"), sep=";", encoding="utf-8")
    df.to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")
elif typeBPEJ == "climate":
    df = pandas.read_csv(files + "/KlimatickyRegion.csv", sep=";", encoding="utf-8")
    df.loc[[int(codeBPEJ[0])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")
elif typeBPEJ == "inclination":
    df = pandas.read_csv(files + "/SklonitostExpozice.csv", sep=";", encoding="utf-8")
    df.loc[[int(codeBPEJ[2])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")
elif typeBPEJ == "soilDepth":
    df = pandas.read_csv(files + "/HloubkaPudySkeletovitost.csv", sep=";", encoding="utf-8")
    df.loc[[int(codeBPEJ[3])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")
elif typeBPEJ == "soilUnit":
    df = None
    soil = open(files + "/HlavniPudniJednotka.csv", "r").read().split('\n')

    lineCode = int(str(codeBPEJ[5]) + str(codeBPEJ[6]))
    
    firstRow = soil.index(str(lineCode), 0, len(soil)) + 1
    lastRow = soil.index(str(lineCode + 1), 0, len(soil))

    #df = pandas.DataFrame([soil[firstRow:lastRow]])
    
    file = open(config.get("Paths", "PipeBPEJinfo"), "w")

    file.write("Popis kódu " + str(codeBPEJ[5]) + str(codeBPEJ[6]) + "\n")
    file.write("\n".join(soil[firstRow:lastRow]))

    file.close()



# df = pandas.read_csv(files + "/HlavniPudniJednotka.csv", sep=";", encoding="utf-8")
# df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")
