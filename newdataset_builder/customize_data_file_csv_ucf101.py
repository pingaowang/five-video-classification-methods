"""
Copy specific lines of the original csv which contains all data, to
a new csv, which contains only selected classes.
"""
from yaml_util import read_list_yaml
import csv
import os.path

## config
# input
original_csv_path = '../data/data_file.csv'
classes_yaml_path = 'ucf_101_motion_classes.yaml'
key_name = 'classes'
# output
output_dir = 'output_csv'
output_file_name = 'ucf101_motion.csv'

def main():
    output_path = os.path.join(output_dir, output_file_name)
    assert not os.path.isfile(output_path), "the output csv exist. Need to rename the output_file_name."
    list_classes = read_list_yaml(classes_yaml_path, key_name)

    csv.register_dialect('ucf101_dialect', delimiter=',', skipinitialspace=True)

    with open(original_csv_path, 'r') as csv_file, open(output_path, 'w') as f_out:
        reader = csv.reader(csv_file, dialect='ucf101_dialect')
        writer = csv.writer(f_out, delimiter=',')
        for row in reader:
            if row[1] in list_classes:
                writer.writerow(row)


if __name__ == '__main__':
    main()



