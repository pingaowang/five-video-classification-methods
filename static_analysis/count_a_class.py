"""
Count how many videos in a class.
"""
import csv
import os.path

csv_path = "./ucf101_motion.csv"
class_name = "TainChi"

csv.register_dialect('ucf101_dialect', delimiter=',', skipinitialspace=True)

with open(csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file, dialect='ucf101_dialect')
    for row in reader:
