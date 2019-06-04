import yaml


def read_list_yaml(yaml_file_path, key):
    list_elements = []
    with open(yaml_file_path, 'r') as stream:
        list_elements = yaml.load(stream)[key]
    return list_elements
