import yaml

config_file = "config.yml"

with open(config_file, 'r') as config_file:
    config = yaml.safe_load(config_file)

def ServerConfig():
    return config['server']

def DatabaseConfig():
    return config['database']

def InterfaceConfig():
    return config['interface']

def EnvironmentConfig():
    return config['environment']
