import logging
from flask import Flask, render_template, request, json
from flask.logging import default_handler
from multiprocessing import Value
from typing import Dict
from src.logger import get_process_logger, flask_logger_config
from src.config import ServerConfig
from src.state import HeaterState
from src.superviser import Superviser

server_config = ServerConfig()

host=server_config['host']
port=server_config['port']
debug=server_config['debug']
tolerance=0.05

state: HeaterState
superviser: Superviser

logger = get_process_logger('server')

app = Flask(__name__)

# Sets the flask logger back to Stream Handler to prevent it from writing into the log file
logging.config.dictConfig(flask_logger_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    global state, superviser, logger
    if request.method == 'POST':
        type = request.form['type']
        if type == '+':
            state.increate_temp_should()
        elif type == '-':
            state.decrease_temp_should()
        elif type == 'onoff':
            state.toggle_running()
            if state.is_running() == True:
                if not superviser.start():
                    return create_json_response(
                        response = {'success': False},
                        status = 500)
            else:
                if not superviser.stop():
                    return create_json_response(
                        response = {'success': False},
                        status = 500)

        logger.log(logging.INFO, "Superviser stopped successfully")
        return create_json_response(
            response = {'success': True},
            status = 200
        )
    elif request.method == 'GET':
        return render_template('main.html', temp_is=state.get_temp_is(), temp_should=state.get_temp_should())

@app.route('/history', methods=['GET'])
def history():
    return None

@app.route('/get_status', methods=['GET'])
def get_status():
    global state
    return create_json_response(
        response = {'success': True, 'temp_should': round_dec_two(state.get_temp_should()), 'running': state.is_running(), 'heating': state.is_heating()},
        status = 200)

@app.route('/get_temp', methods=['GET'])
def get_curr_temp():
    global state
    return create_json_response(
        response = {'success': True, 'temp_is': round_dec_two(state.get_temp_is())},
        status = 200)

@app.route('/temperatur', methods=['GET'])
def get_curr_temps():
    global temp_is, temp_should
    temps = get_temps()
    temp_is.value = get_temperature()
    return create_json_response(
        response = {'temp_is': temp_is.value, 'temp_should': temp_should.value, '1': temps[0],'2': temps[1],'3': temps[2],'4': temps[3]},
        status = 200)


def round_dec_two(value: float):
    return round(value, 2)

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response


def main():
    global state, superviser, logger

    temp_is = Value('d')
    temp_should = Value('d')
    running = Value('b')
    heating = Value('b')
    temp_should.value = 40.0
    running.value = False
    heating.value = False

    state = HeaterState(temp_is=temp_is, should=temp_should, running=running, heating=heating)
    state.turn_off_heating()

    superviser = Superviser(state=state, logger=logger)

    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    main()
