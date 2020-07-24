#!/usr/bin/env python3.7
import pandas
import configparser
import sys

config = configparser.ConfigParser()
config.read("/home/pi/Documents/OGSatGitHub/config.conf")

files = config.get("Paths", "FilesBPEJ")


df = pandas.read_csv(files + "/KlimatickyRegion.csv", sep=";", encoding="utf-8")
print(df.loc[[int(sys.argv[1])]].to_csv(config.get("Paths", "PipeBPEJinfo"), header=True, index=False, sep=";", quoting=None))