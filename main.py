import logging
from flask import Flask, render_template, request, json
from flask.logging import default_handler
from flask_socketio import SocketIO, emit
from multiprocessing import Value
from typing import Dict
from src.logger import get_process_logger, flask_logger_config
from src.config import ServerConfig
from src.state import HeaterState
from src.superviser import Superviser
from src.socket import StateSocket
from src.history import DBConnection
from src.historySocket import HistorySocket
from src.utils import round_dec_two

server_config = ServerConfig()

host=server_config['host']
port=server_config['port']
debug=server_config['debug']
tolerance=0.05

state: HeaterState
superviser: Superviser

logger = get_process_logger('server')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'

socketio = SocketIO(app, logger=True, engineio_logger=True)
status_socket = StateSocket('/state')
socketio.on_namespace(status_socket)
history_socket = HistorySocket('/history')
socketio.on_namespace(history_socket)

# Sets the flask logger back to Stream Handler to prevent it from writing into the log file
logging.config.dictConfig(flask_logger_config)

@app.route('/', methods=['GET'])
def index():
    global state, superviser, logger
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
        superviser.start()
    else:
        superviser.stop()

    logger.log(logging.INFO, "Superviser stopped successfully")

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response

def main():
    global state, superviser, logger, status_socket

    temp_is = Value('d')
    temp_should = Value('d')
    running = Value('b')
    heating = Value('b')
    temp_should.value = 40.0
    running.value = False
    heating.value = False

    db_conn = DBConnection()
    db_conn.prepare_tables()


    state = HeaterState(temp_is=temp_is, should=temp_should, running=running, heating=heating)
    state.turn_off_heating()

    superviser = Superviser(state=state, logger=logger)

    status_socket._state = state
    status_socket._start_stop_superviser = manage_superviser

    history_socket._state = state

    # app.run(host=host, port=port, debug=debug, use_reloader=False)
    socketio.run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
