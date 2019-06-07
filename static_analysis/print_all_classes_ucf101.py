"""
A small script to print all classes's names: str of UCF-101 dataset.
"""
from yaml_util import read_list_yaml
import csv
import os.path

## exp_run_config
# input
original_csv_path = '../data/ucf101.csv'

csv.register_dialect('ucf101_dialect', delimiter=',', skipinitialspace=True)
list_classes_ucf101 = []

with open(original_csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file, dialect='ucf101_dialect')
    for row in reader:
        if not row[1] in list_classes_ucf101:
            list_classes_ucf101.append(row[1])
sorted_list = sorted(list_classes_ucf101)
for ele in sorted_list:
    print(ele)



