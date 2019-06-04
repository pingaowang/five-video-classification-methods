import argparse
import os.path

##-- args --##
parser = argparse.ArgumentParser()
parser.add_argument("config", type=str, help="config file's name")
args = parser.parse_args()