import time
import logging
from multiprocessing import Process, Value
from flask import Flask, render_template, request, json
from flask.logging import default_handler
from typing import Dict
from src.heatcontrol import get_temperature, turn_on_heating, turn_off_heating, get_temps
from src.logger import get_process_logger, flask_logger_config

host='0.0.0.0'
port='80'
debug=True
tolerance=0.05

temp_is = Value('d')
temp_should = Value('d')
running = Value('b')
heating = Value('b')
superviser: Process

logger = get_process_logger('server')

app = Flask(__name__)
logging.config.dictConfig(flask_logger_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    global temp_is, temp_should, running, heating, superviser, logger

    if request.method == 'POST':
        type = request.form['type']
        if type == '+':
            temp_should.value += 1.0
        elif type == '-':
            temp_should.value -= 1.0
        elif type == 'onoff':
            running.value = not running.value
            if running.value == True:
                if superviser == None:
                    superviser = Process(target=supervise, args=(temp_is, temp_should, running, heating))
                    try:
                        superviser.start()
                    except RuntimeError:
                        superviser = None
                        logger.log(logging.ERROR, "Cannot stop process - Process already running")
                        return create_json_response(
                            response = {'success': False, 'reason': 'Process already running'},
                            status = 500)
            else:
                try:
                    superviser.join(timeout=5)
                    if superviser is not None and superviser.is_alive():
                        logger.log(logging.ERROR, "Cannot stop process - Still alive after timeout")
                        return create_json_response(
                            response = {'success': False, 'reason': 'Failed to stop process.'},
                            status = 500)
                    superviser = None
                    turn_off_heating()
                    heating.value = False
                except RuntimeError:
                    logger.log(logging.ERROR, "Cannot stop process - Process wasn't running")
                    return create_json_response(
                        response = {'success': False, 'reason': 'Cannot stop. Process not running.'},
                        status = 500)

        logger.log(logging.INFO, "Superviser stopped successfully")
        return create_json_response(
            response = {'success': True},
            status = 200
        )
    elif request.method == 'GET':
        return render_template('main.html', temp_is=temp_is.value, temp_should=temp_should.value)


def round_dec_two(value: float):
    return round(value, 2)

@app.route('/get_status', methods=['GET'])
def get_status():
    global temp_should, running, heating
    return create_json_response(
        response = {'success': True, 'temp_should': round_dec_two(temp_should.value), 'running': running.value, 'heating': heating.value},
        status = 200)

@app.route('/get_temp', methods=['GET'])
def get_curr_temp():
    global temp_is, temp_should, running
    return create_json_response(
        response = {'success': True, 'temp_is': round_dec_two(temp_is.value)},
        status = 200)

@app.route('/temperatur', methods=['GET'])
def get_curr_temps():
    global temp_is, temp_should
    temps = get_temps()
    temp_is.value = get_temperature()
    return create_json_response(
        response = {'temp_is': temp_is.value, 'temp_should': temp_should.value, '1': temps[0],'2': temps[1],'3': temps[2],'4': temps[3]},
        status = 200)

def supervise(temp_is, temp_should, running, heating):
    logger = get_process_logger('superviser')
    logger.log(logging.INFO, "Superviser process started")
    while(running.value):
        temp_is.value = get_temperature()
        temp_is_rounded = int(round(temp_is.value))
        if (temp_is_rounded < (temp_should.value - temp_should.value * tolerance)):
            turn_on_heating()
            heating.value = True
        elif (temp_is_rounded >= temp_should.value):
            turn_off_heating()
            heating.value = False
        time.sleep(30)

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response


def main():
    global temp_is, temp_should, running, heating, superviser

    temp_is.value = get_temperature()
    temp_should.value = 40.0
    running.value = False
    heating.value = False

    turn_off_heating()

    superviser = None

    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    main()
