import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'conf' / 'config.yaml'


def get_config(path):
    with open(path) as fd:
        config = yaml.safe_load(fd)
        return config


config = get_config(config_path)
