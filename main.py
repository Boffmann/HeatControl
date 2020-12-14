import time
import multiprocessing
from flask import Flask, render_template, request, json

host='127.0.0.1'
port='80'
debug=True

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
        print(type)
        if type == '+':
            temp_should.value += 1
        elif type == '-':
            temp_should.value -= 1
        elif type == 'onoff':
            running.value = not running.value
            if running.value == True:
                superviser.start()
            else:
                superviser.join()
                superviser = multiprocessing.Process(target=supervise, args=(temp_is, temp_should, running))


        return json.dumps({'status': 'OK', 'temp_should': temp_should.value, 'running': running.value})
    elif request.method == 'GET':
        return render_template('main.html', temp_is=temp_is.value, temp_should=temp_should.value, reload = time.time())

@app.route('/temp_is', methods=['GET'])
def get_temp_is():
    global temp_is
    response = app.response_class(
        response=json.dumps({'success': True, 'value': temp_is.value}),
        status=200,
        mimetype='application/json'
    )
    return response

def supervise(temp_is, temp_should, running):
    while(running.value):
        temp_is.value += 1
        print("Value")
        print(temp_should.value)
        print(temp_is.value)
        time.sleep(1)

def main():
    global temp_is, temp_should, running, superviser

    temp_is.value = 20
    temp_should.value = 40
    running.value = True
    print("Main")

    superviser = multiprocessing.Process(target=supervise, args=(temp_is, temp_should, running))

    superviser.start()

    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    main()
