from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import time
import threading

command = "Hello"


start_time = time.time()
lock = threading.Lock()

def change_command(data):
    global command
    command = data

def start_existing_server(host, port):
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)

    print(f"Existing Server listening on {host}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

def start_commented_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Commented Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")

        change_command(data)

        response = "Hello from commented server!"
        client_socket.send(response.encode('utf-8'))

        client_socket.close()

def start_servers(host, port_existing, port_commented):
    existing_server_thread = threading.Thread(target=start_existing_server, args=(host, port_existing), daemon=True)
    existing_server_thread.start()

    commented_server_thread = threading.Thread(target=start_commented_server, args=(host, port_commented), daemon=True)
    commented_server_thread.start()

    # Wait for all threads to finish
    existing_server_thread.join()
    commented_server_thread.join()

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


if __name__ == "__main__":
    host = "127.0.0.1"
    port_existing = 5000
    port_commented = 12345
    start_servers(host, port_existing, port_commented)
