import threading
from typing import Callable
from ..utils.listener import Listener
from ..utils.connection import Connection
from ..utils.protocol import Hello, Config, Snapshot
# from ..utils.parser import Parser


FIELDS = ['pose', 'color_image', 'depth_image']


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection: Connection, publish: Callable[[str], None], parsers: dict):
        super(Handler, self).__init__()
        self.connection = connection
        self.publish = publish
        self.parsers = parsers

    def run(self):
        with self.connection as connection:
            hello = Hello.deserialize(connection.receive())
            print(hello)
            config = Config(FIELDS)
            connection.send(config.serialize())
            snapshot = Snapshot.deserialize(connection.receive(), config.fields)
            print(snapshot.timestamp)
        Handler.lock.acquire()
        try:
            pass
            # for name, parser in self.parsers.items():
            #     parse_result = parser.parse(hello.user.user_id, snapshot)
            #     self.publish(parse_result)
        finally:
            Handler.lock.release()


def run_server(host: str, port: int, publish=print):
    # parsers = {key: cls() for key, cls in Parser.parsers.items() if key in FIELDS}
    with Listener(port, host=host) as listener:
        print(f'Listening on {host}:{port}')
        while True:
            connection = listener.accept()
            # handler = Handler(connection, data_dir, parsers)
            handler = Handler(connection, publish, {})
            handler.start()
