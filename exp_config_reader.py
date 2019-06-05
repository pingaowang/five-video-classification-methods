from argments import args
import os.path
import yaml


def get_config(config_path):
    assert os.path.isfile(config_path), "the exp_run_config yaml file doesn't exist."
    with open(str(config_path), 'r') as stream:
        data_loaded: dict = yaml.safe_load(stream)
    return data_loaded


config_name = args.exp_run_config
config_path = os.path.join('exp_run_config', config_name + '.yaml')
config = get_config(config_path)

## get env var from configs
# Experiment info
EXP_NAME = config['exp_name']

# Load saved model exp_run_config
IS_USING_SAVED_MODEL = config['is_using_saved_model']

if IS_USING_SAVED_MODEL:
    SAVED_MODEL = config['saved_model_path']
else:
    SAVED_MODEL = None

# Dataset exp_run_config:
DATA_CSV_PATH = config['data_csv_path']

# Model exp_run_config
MODEL = config['model']
BATCH_SIZE = config['batch_size']
SEQ_LENGTH = config['seq_length']
MAX_EPOCH = config['max_epoch']
PATIENTS = config['patients']


