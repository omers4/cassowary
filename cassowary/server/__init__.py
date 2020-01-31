import json
import threading
from ..utils.listener import Listener
from ..utils.connection import Connection
from ..utils.protocol import Hello, Config, Snapshot


FIELDS = ['pose', 'color_image', 'depth_image']


def dump_snapshot(user_id, snapshot):
    # TODO: dump the image data to raw files, if there is data a all
    # TODO test all parser
    # TODO Write a tutorial for a new parser
    # TODO write unit tests for parsing
    # TODO fields should be configurable... or, just send them all...

    return json.dumps({
        'user_id': user_id,
        'timestamp': snapshot.timestamp,
        'rotation': snapshot.rotation,
        'translation': snapshot.translation})


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection: Connection, publish):
        super(Handler, self).__init__()
        self.connection = connection
        self.publish = publish

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
            to_publish = dump_snapshot(hello.user.user_id, snapshot)
            self.publish(to_publish)
        finally:
            Handler.lock.release()


def run_server(host: str, port: int, publish=print):
    with Listener(port, host=host) as listener:
        print(f'Listening on {host}:{port}')
        while True:
            connection = listener.accept()
            handler = Handler(connection, publish)
            handler.start()
