import logging
from flask import Flask, render_template, request, json
from flask_socketio import SocketIO, emit
from multiprocessing import Value
from typing import Dict
import src.logging as mylogger
from src.config import ServerConfig
from src.state import HeaterState
from src.superviser import Superviser
from src.socket import StateSocket
from src.history import DBConnection
from src.utils import round_dec_two, get_curr_time

server_config = ServerConfig()

host=server_config['host']
port=server_config['port']
debug=server_config['debug']
tolerance=0.05

state: HeaterState
superviser: Superviser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'

socketio = SocketIO(app, logger=True, engineio_logger=True)
status_socket = StateSocket('/state')
socketio.on_namespace(status_socket)

@app.route('/', methods=['GET'])
def index():
    global state, superviser
    return render_template('main.html', temp_is=state.get_temp_is(), temp_should=state.get_temp_should())

@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html')

@app.route('/temperatur', methods=['GET'])
def get_curr_temps():
    global temp_is, temp_should
    temps = get_temps()
    temp_is.value = get_temperature()
    return create_json_response(
        response = {'temp_is': temp_is.value, 'temp_should': temp_should.value, '1': temps[0],'2': temps[1],'3': temps[2],'4': temps[3]},
        status = 200)

def manage_superviser():
    global state
    if state.is_running() == True:
        if superviser.start():
            status_socket.set_starttime(get_curr_time())
    else:
        superviser.stop()

    mylogger.info("Superviser stopped successfully")

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response

def main():
    global state, superviser, status_socket

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
    state.turn_off_heating()

    superviser = Superviser(state=state)

    status_socket._state = state
    status_socket._start_stop_superviser = manage_superviser
    status_socket.set_starttime(get_curr_time())

    # app.run(host=host, port=port, debug=debug, use_reloader=False)
    socketio.run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
