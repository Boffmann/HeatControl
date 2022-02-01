import logging
from flask import Flask, render_template, json
from flask_socketio import SocketIO
from multiprocessing import Value
from typing import Dict
from heatcontrol.config import ServerConfig
from heatcontrol.test_state import HeaterState
from heatcontrol.socket import StateSocket
from heatcontrol.history import DBConnection
#from heatcontrol.heatcontrol import get_temps, get_temperature


server_config = ServerConfig()

host=server_config['host']
port=server_config['port']
debug=server_config['debug']
tolerance=0.05

state: HeaterState
temp_is: Value
temp_should: Value

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'

socketio = SocketIO(app, logger=True, engineio_logger=True)
status_socket = StateSocket('/state')
socketio.on_namespace(status_socket)

@app.route('/', methods=['GET'])
def index():
    global state
    return render_template('main.html', temp_is=state.get_temp_is(), temp_should=state.get_temp_should())

@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html')

"""@app.route('/temperatur', methods=['GET'])
def get_curr_temps():
    global temp_is, temp_should
    temps = get_temps()
    temp_is.value = get_temperature()
    return create_json_response(
        response = {'temp_is': temp_is.value, 'temp_should': temp_should.value, '1': temps[0],'2': temps[1]},
        status = 200)"""

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response

def main():
    global state, status_socket

    temp_is = Value('d')
    temp_should = Value('d')
    running = Value('b')
    heating = Value('b')

    temp_should.value = 40.0
    running.value = False
    heating.value = False

    db_conn = DBConnection()
    db_conn.prepare_tables()
    db_conn.close()

    state = HeaterState(temp_is=temp_is, should=temp_should, running=running, heating=heating)

    status_socket.initialize(state)

    socketio.run(app, host=host, port=port, debug=debug)

    state.connect_to_socket()

if __name__ == '__main__':
    main()
