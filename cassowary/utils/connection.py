import io
import socket
import struct


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        local_ip, local_port = self.socket.getsockname()
        peer_ip, peer_port = self.socket.getpeername()
        return f'<Connection from {local_ip}:{local_port}' \
               f' to {peer_ip}:{peer_port}>'

    def send(self, data):
        self.socket.sendall(struct.pack('I', len(data)))
        self.socket.sendall(data)

    def _receive_by_size(self, size):
        length_to_read = size
        data_chunks = []
        while True:
            data = self.socket.recv(length_to_read)
            if not data:
                break
            data_chunks.append(data)
            length_to_read -= len(data)
        data = b''.join(data_chunks)
        if length_to_read > 0:
            raise Exception('Connection was interrupted')
        return data

    def receive(self):
        msg_len_bytes = self.socket.recv(4)
        msg_len = struct.unpack('I', msg_len_bytes)[0]
        return io.BytesIO(self._receive_by_size(msg_len))

    @classmethod
    def connect(cls, ip, port):
        conn = socket.socket()
        conn.connect((ip, port))
        return Connection(conn)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.socket.close()


# with Connection.connect('127.0.0.1', 8800) as c:
#     print(c)
