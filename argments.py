import argparse
import os.path

##-- args --##
parser = argparse.ArgumentParser()
parser.add_argument("exp_run_config", type=str, help="exp_run_config file's name")
args = parser.parse_args()