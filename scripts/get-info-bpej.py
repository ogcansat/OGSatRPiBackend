#!/usr/bin/env python3.7
import pandas
import configparser
import sys

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

files = config.get("Paths", "FilesBPEJ")

codeBPEJ = sys.argv[1]


df = pandas.read_csv(files + "/KlimatickyRegion.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[0])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="w")

df = pandas.read_csv(files + "/SklonitostExpozice.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[2])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")

df = pandas.read_csv(files + "/HloubkaPudySkeletovitost.csv", sep=";", encoding="utf-8")
df.loc[[int(codeBPEJ[3])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")

# df = pandas.read_csv(files + "/HlavniPudniJednotka.csv", sep=";", encoding="utf-8")
# df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8", mode="a")
