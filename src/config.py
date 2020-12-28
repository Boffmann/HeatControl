import yaml
import pathlib

this_dir = pathlib.Path(__file__).parent.absolute()
config_file = str(this_dir) + "/../config.yml"
print(config_file)

with open(config_file, 'r') as config_file:
    config = yaml.load(config_file)

def ServerConfig():
    return config['server']
