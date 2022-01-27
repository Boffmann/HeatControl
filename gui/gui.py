from turtle import bgcolor
import PySimpleGUI as sg
import paramiko as pm
import time
from paramiko import BadHostKeyException, AuthenticationException
import yaml
from os import path
from sys import exit

txt_color = "#282828"
button_color = "#458588"

def create_popup(text):

    bg_color = "#d79921"

    layout = [
        [sg.Text(text, font=('Any 15'), background_color=bg_color, text_color=txt_color)],
        [sg.Column(
            [[sg.Button('OK', size=(10, 1), font=('Any 15'), button_color=(txt_color, button_color))]],
            justification='center')]
    ]
    
    window = sg.Window('INFO', layout, margins=(50, 25), background_color=bg_color)
    
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
        create_popup("Cound not open/read ~/.heat_control_ssh.yml. Are you sure the file exists?")
        exit()
    return (host, port, username, password)


def execute_ssh_command(command):
    """
    https://www.ivankrizsan.se/2016/04/24/execute-shell-commands-over-ssh-using-python-and-paramiko/
    """
    host, port, username, password = parse_ssh_config()
    ssh = None

    try:        
        ssh = pm.SSHClient()
        ssh.set_missing_host_key_policy(pm.AutoAddPolicy())

        ssh.connect(host, port, username, password)
    
        stdin, stdout, stderr = ssh.exec_command(command)

        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)

        return stdout.channel.recv_exit_status()
    except BadHostKeyException:
        create_popup("HeatControl server's host key cound not be verified")
    except AuthenticationException:
        create_popup("Authenticating with HeatControl server failed. Wrong Username/Password?")
    except Exception:
        create_popup("An unknown error occured while connecting to HeatControl server or executing a command")
    finally:
        if ssh is not None:
            ssh.close()

def start_service():
    exit_code = execute_ssh_command("start_heat_control")
    if exit_code == 0:
        create_popup("Started HeatControl")
    elif exit_code == 1:
        create_popup("Error: Could not start HeatControl. Server already running.")
    else:
        create_popup("Error: Could not start HeatControl.")

def stop_service():
    exit_code = execute_ssh_command("stop_heat_control")
    if exit_code == 0:
        create_popup("Stopped HeatControl")
    elif exit_code == 1:
        create_popup("Error: Could not stop HeatControl. Server is not running.")
    else:
        create_popup("Error: Could not stop HeatControl.")


layout = [[
        sg.Button("Start Service", size=(10, 2), font=('Any 15'), button_color=(txt_color, button_color)),
        sg.Button("Stop Service",  size=(10, 2), font=('Any 15'), button_color=(txt_color, button_color))
    ]]

window = sg.Window(title="HeatControl", layout=layout, margins=(100, 50), background_color="#98971a").Finalize()

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Start Service":
        start_service()
    elif event == "Stop Service":
        stop_service()

window.close()