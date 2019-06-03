import argparse
import os.path

##-- args --##
parser = argparse.ArgumentParser()
parser.add_argument("config", type=str, help="config file's name")
args = parser.parse_args()

config_name = args.config
CONFIG_PATH = os.path.join('config', config_name + '.yaml')