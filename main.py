import time
import multiprocessing
from flask import Flask, render_template, request, json
from typing import Dict
from src.heatcontrol import get_temperature, turn_on_heating, turn_off_heating

host='0.0.0.0'
port='80'
debug=True
tolerance = 0.05

temp_is = multiprocessing.Value('i')
temp_should = multiprocessing.Value('i')
running = multiprocessing.Value('b')
superviser: multiprocessing.Process

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global temp_is, temp_should, running, superviser

    if request.method == 'POST':
        type = request.form['type']
        if type == '+':
            temp_should.value += 1
        elif type == '-':
            temp_should.value -= 1
        elif type == 'onoff':
            running.value = not running.value
            if running.value == True:
                if superviser == None:
                    superviser = multiprocessing.Process(target=supervise, args=(temp_is, temp_should, running))
                    try:
                        superviser.start()
                    except RuntimeError:
                        superviser = None
                        return create_json_response(
                            response = {'success': False, 'reason': 'Process already running'},
                            status = 500)
            else:
                try:
                    superviser.join(timeout=5)
                    if superviser is not None and superviser.is_alive():
                        return create_json_response(
                            response = {'success': False, 'reason': 'Failed to stop process.'},
                            status = 500)
                    superviser = None
                except RuntimeError:
                    return create_json_response(
                        response = {'success': False, 'reason': 'Cannot stop. Process not running.'},
                        status = 500)

        return create_json_response(
            response = {'success': True},
            status = 200
        )
    elif request.method == 'GET':
        return render_template('main.html', temp_is=temp_is.value, temp_should=temp_should.value)

@app.route('/get_status', methods=['GET'])
def get_status():
    global temp_is, temp_should, running
    return create_json_response(
        response = {'success': True, 'temp_is': temp_is.value, 'temp_should': temp_should.value, 'running': running.value},
        status = 200)

def supervise(temp_is, temp_should, running):
    while(running.value):
        temp_is.value = get_temperature()
        if (temp_is.value < (temp_should.value - temp_should.value * tolerance)):
            turn_on_heating()
        else:
            turn_off_heating()
        time.sleep(1)

def create_json_response(response: Dict[str, object], status: int):
    response = app.response_class(
        response=json.dumps(response),
        status=status,
        mimetype='application/json'
    )
    return response


def main():
    global temp_is, temp_should, running, superviser

    temp_is.value = get_temperature()
    temp_should.value = 40
    running.value = False

    superviser = None

    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    main()
