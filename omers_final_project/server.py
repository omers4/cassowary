import datetime
import os
import struct
import threading

from .utils.listener import Listener
from .utils.connection import Connection
from .utils.protocol import Hello, Config, Snapshot
from .utils.parser import Parser


FORMAT = 'LLI'
PACK_SIZE = struct.calcsize('LLI')

FIELDS = ['translation', 'color_image']


def save_user_data(thought_obj, data_dir):
    date_repr = str(datetime.datetime.fromtimestamp(thought_obj.timestamp))\
        .replace(' ', '_').replace(':', '-')
    filepath = f'{data_dir}/{thought_obj.user_id}/{date_repr}.txt'
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    add_space = os.path.exists(filepath)
    with open(filepath, 'a') as f:
        if add_space:
            f.write('\n')
        f.write(thought_obj.thought)


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection: Connection, data_dir: str):
        super(Handler, self).__init__()
        self.connection = connection
        self.data_dir = data_dir
        self.parsers = {key: cls(data_dir) for key, cls in Parser.parsers.items() if key in FIELDS}

    def run(self):
        with self.connection as connection:
            hello = Hello.deserialize(connection.receive())
            print(hello)
            config = Config(FIELDS)
            connection.send(config.serialize())
            snapshot = Snapshot.deserialize(connection.receive(), config.fields)
        Handler.lock.acquire()
        try:
            for name, parser in self.parsers.items():
                parser.parse(hello.user.user_id, snapshot)
        finally:
            Handler.lock.release()


def run_server(address, data_dir):
    ip, port = address
    with Listener(port, host=ip) as listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, data_dir)
            handler.start()
