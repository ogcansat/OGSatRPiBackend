#!/usr/bin/env python3.7
import pandas
import configparser
import sys
import subprocess

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

files = config.get("Paths", "FilesBPEJ")

codeBPEJ = sys.argv[1]

subprocess.call(["python3.7", config.get("Paths", "PlantScript"), codeBPEJ])
df = pandas.read_csv(config.get("Paths", "PipePlant"), sep=";", encoding="utf-8")
df.to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")

#df = pandas.DataFrame({"Bříza bělokorá (strom)": ["Pravděpodobnost: 80%"]})
#df.to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")

df = pandas.read_csv(files + "/KlimatickyRegion.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[0])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")

df = pandas.read_csv(files + "/SklonitostExpozice.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[2])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")

df = pandas.read_csv(files + "/HloubkaPudySkeletovitost.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[3])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")

soil = open(files + "/HlavniPudniJednotka.csv", "r").read().split('\n')
df = pandas.DataFrame({soil[0]: [soil[1]]})
df.to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")


# df = pandas.read_csv(files + "/HlavniPudniJednotka.csv", sep=";", encoding="utf-8")
# df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")
