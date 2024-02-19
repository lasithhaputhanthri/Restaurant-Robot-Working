from flask import Flask, request, jsonify
import schedule
import time

app = Flask(__name__)

command = "Hello"

start_time = time.time()

def change_command():
    global command
    if command == "Hello":
        command = "Bye"
    else:
        command = "Hello"

@app.route('/api_endpoint', methods=['GET', 'POST'])
def handle_api_request():

    # Schedule a job to change the command every 5 seconds
    global start_time
    millis = int(round(time.time() * 1000))
    if millis - start_time > 1000:
        start_time = millis
        change_command()

    if request.method == 'GET':
        result = {"message": "Received command successfully", "command": command}
    elif request.method == 'POST':
        data = request.get_json()
        result = {"message": "Received data successfully", "data": data}
    else:
        result = {"error": "Unsupported request method"}

    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask application on all available network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)