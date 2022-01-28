from turtle import bgcolor
import PySimpleGUI as sg
import paramiko as pm
import time
from paramiko import BadHostKeyException, AuthenticationException
from enum import Enum
import yaml
from os import path
from sys import exit

TXT_COLOR = "#282828"
BUTTON_COLOR = (TXT_COLOR, "#458588")
FONT = ('Any 15')
CONFIG_FILE = path.expanduser('~') + "/.heat_control_ssh.yml"
INFO_COLOR = "#689d6a"
WARNING_COLOR = "#d79921"
ERROR_COLOR = "#cc241d"

class CommandExecutionException(BaseException):
    pass

class PopupType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def create_popup(text, type: PopupType):
    popup_bg_color = INFO_COLOR if type is PopupType.INFO else WARNING_COLOR if type is PopupType.WARNING else ERROR_COLOR

    layout = [
        [sg.Text(text, font=FONT, background_color=popup_bg_color, text_color=TXT_COLOR)],
        [sg.Column(
            [[sg.Button('OK', size=(10, 1), font=FONT, button_color=BUTTON_COLOR)]], justification='center')]
    ]
    
    popup_window = sg.Window(type.name, layout, margins=(50, 25), background_color=popup_bg_color)
    popup_window.read()
    popup_window.close()

def parse_ssh_config():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config = yaml.safe_load(config_file)
            host = config['host']
            port = config['port']
            username = config['username']
            password = config['password']
    except OSError:
        create_popup("Cound not open/read " + CONFIG_FILE + ". Are you sure the file exists?", PopupType.ERROR)
        exit()
    return (host, port, username, password)


def execute_ssh_command(command):
    """
    https://www.ivankrizsan.se/2016/04/24/execute-shell-commands-over-ssh-using-python-and-paramiko/
    """
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
        raise CommandExecutionException("HeatControl server's host key cound not be verified")
    except AuthenticationException:
        raise CommandExecutionException("Authenticating with HeatControl server failed. Wrong Username/Password?")
    except Exception:
        raise CommandExecutionException("Error: Could not connect to Raspberry Pi \"" + username + "@" + host + "\"")
    finally:
        if ssh is not None:
            ssh.close()

def start_service():
    try:
        exit_code = execute_ssh_command("start_heat_control")
    except CommandExecutionException as e:
        create_popup(e)

    if exit_code == 0:
        create_popup("Started HeatControl", PopupType.INFO)
    elif exit_code == 1:
        create_popup("Could not start HeatControl. Server already running.", PopupType.WARNING)
    else:
        create_popup("Could not start HeatControl.", PopupType.ERROR)

def stop_service():
    try:
        exit_code = execute_ssh_command("stop_heat_control")
    except CommandExecutionException as e:
        create_popup(e, PopupType.ERROR)
    
    if exit_code == 0:
        create_popup("Stopped HeatControl", PopupType.INFO)
    elif exit_code == 1:
        create_popup("Could not stop HeatControl. Server is not running.", PopupType.WARNING)
    else:
        create_popup("Error: Could not stop HeatControl.", PopupType.ERROR)


host, port, username, password = parse_ssh_config()

layout = [[
        sg.Button("Start Service", size=(10, 2), font=FONT, button_color=BUTTON_COLOR),
        sg.Button("Stop Service",  size=(10, 2), font=FONT, button_color=BUTTON_COLOR)
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
