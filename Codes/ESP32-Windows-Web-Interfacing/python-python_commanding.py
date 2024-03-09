import zmq

while(True):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    socket.send(b"Hello from script1!")
    print("running")