"""
Count how many videos in a class.
"""
import csv
import os.path

csv_path = "../data/ucf101_motion.csv"
class_name = "Swing"
train_test = "test"

csv.register_dialect('ucf101_dialect', delimiter=',', skipinitialspace=True)

with open(csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file, dialect='ucf101_dialect')
    count = 0
    for row in reader:
        if row[0] == train_test and row[1] == class_name:
            print(row)
            count += 1

print(count)
