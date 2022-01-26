import PySimpleGUI as sg
import paramiko as pm
import time
import yaml
from os import path
from sys import exit

def create_popup(text):

    layout = [
        [sg.Text(text, font=('Any 15'))],
        [sg.Button('OK', size=(10, 1))]
    ]
    
    window = sg.Window('INFO', layout, margins=(50, 25))
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "OK":
            break

    window.close()

def parse_ssh_config():
    home_dir = path.expanduser('~')
    config_file = home_dir + "/.heat_control_ssh.yml"
    try:
        with open(config_file, 'r') as config_file:
            config = yaml.safe_load(config_file)
            host = config['host']
            port = config['port']
            username = config['username']
            password = config['password']
    except OSError:
        create_popup("Cound not open/read ssh config file. Are you sure the file exists?")
        exit()
    return (host, port, username, password)


def execute_ssh_command(command):
    """
    https://www.ivankrizsan.se/2016/04/24/execute-shell-commands-over-ssh-using-python-and-paramiko/
    """
    host, port, username, password = parse_ssh_config()
    ssh = None

    try:        
        ssh = pm.SSHClient
        ssh.set_missing_host_key_policy(pm.AutoAddPolicy())

        ssh.connect(host, port, username, password)
    
        stdin, stdout, stderr = ssh.exec_command(command)

        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)

        stdoutstring = stdout.readlines()
        stderrstring = stderr.readlines()
    finally:
        if ssh is not None:
            ssh.close()

    return stdoutstring, stderrstring

def start_service():
    execute_ssh_command("start_heat_control")

def stop_service():
    execute_ssh_command("stop_heat_control")


layout = [[sg.Button("Start Service", size=(10, 2)), sg.Button("Stop Service", size=(10, 2))]]

window = sg.Window(title="HeatControl", layout=layout, margins=(100, 50)).Finalize()

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Start Service":
        start_service()
    elif event == "Stop Service":
        stop_service()

window.close()