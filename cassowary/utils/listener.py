import socket

from .connection import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = None

    def __repr__(self):
        return f"Listener(port={self.port}, " \
               f"host='{self.host}', " \
               f"backlog={self.backlog}, " \
               f"reuseaddr={self.reuseaddr})"

    def start(self):
        sock = socket.socket()
        if self.reuseaddr:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(self.backlog)
        self.socket = sock

    def stop(self):
        self.socket.close()

    def accept(self):
        client, address = self.socket.accept()
        return Connection(client)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
