import socket
import time

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input("Enter message: ")
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345
    while True:
        start_client(host, port)
        time.sleep(0.500)
