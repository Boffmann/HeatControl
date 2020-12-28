import yaml

config_file = "config.yml"

with open(config_file, 'r') as config_file:
    config = yaml.load(config_file)

def ServerConfig():
    return config['server']
