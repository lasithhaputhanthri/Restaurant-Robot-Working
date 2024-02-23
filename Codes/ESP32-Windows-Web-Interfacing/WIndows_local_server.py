from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import threading

command = "Hello"
start_time = time.time()
lock = threading.Lock()

def change_command():
    global command
    if command == "Hello":
        command = "Bye"
    else:
        command = "Hello"

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message, data=None):
        response = {
            "message": message,
            "command": command if self.command_request() else None,
            "data": data if self.data_request() else None
        }
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def command_request(self):
        return self.path == '/api_endpoint' and self.command == 'GET'

    def data_request(self):
        return self.path == '/api_endpoint' and self.command == 'POST'

    def do_GET(self):
        if self.command_request():
            self._send_response("Received command successfully")

    def do_POST(self):
        if self.data_request():
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_data)
                self._send_response("Received data successfully", data)
            except json.JSONDecodeError:
                self._send_response("Error decoding JSON", None)

def schedule_task():
    while True:
        time.sleep(5)
        with lock:
            change_command()

if __name__ == '__main__':
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, RequestHandler)

    # Start a separate thread for the scheduled task
    task_thread = threading.Thread(target=schedule_task, daemon=True)
    task_thread.start()

    print('Starting server on port 5000...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
