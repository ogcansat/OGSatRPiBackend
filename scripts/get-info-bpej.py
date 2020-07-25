#!/usr/bin/env python3.7
import pandas
import configparser
import sys

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

files = config.get("Paths", "FilesBPEJ")

typeBPEJ = sys.argv[1]
codeBPEJ = int(sys.argv[2])

if typeBPEJ == "climate":
    df = pandas.read_csv(files + "/KlimatickyRegion.csv", sep=";", encoding="utf-8")
    df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8")
elif typeBPEJ == "inclination":
    df = pandas.read_csv(files + "/SklonitostExpozice.csv", sep=";", encoding="utf-8")
    df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8")
elif typeBPEJ == "soil_depth":
    df = pandas.read_csv(files + "/HloubkaPudySkeletovitost.csv", sep=";", encoding="utf-8")
    df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8")
elif typeBPEJ == "soil_unit":
    df = pandas.read_csv(files + "/HlavniPudniJednotka.csv", sep=";", encoding="utf-8")
    df.loc[[codeBPEJ]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None, encoding="utf-8")

