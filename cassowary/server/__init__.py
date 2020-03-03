import json
import struct
import threading
from ..utils.listener import Listener
from ..utils.connection import Connection
from ..utils.protocol import Hello, Config, Snapshot
from . import utils


FIELDS = ['pose', 'feelings', 'color_image', 'depth_image']


def dump_snapshot(user, snapshot):
    w, h, data = snapshot.image
    d_w, d_h, d_data = snapshot.image_depth

    dir_path = '/tmp/parsed_results'
    utils.create_path_dirs(dir_path)
    raw_color_path = utils.get_path(dir_path, user.user_id, snapshot.timestamp, 'raw_color_image')
    raw_depth_path = utils.get_path(dir_path, user.user_id, snapshot.timestamp, 'raw_depth_image')
    color_path = utils.get_path(dir_path, user.user_id, snapshot.timestamp, 'color_image.jpg')
    depth_path = utils.get_path(dir_path, user.user_id, snapshot.timestamp, 'depth_image.jpg')
    with open(raw_color_path, 'wb') as f:
        f.write(data)
    with open(raw_depth_path, 'wb') as f:
        f.write(struct.pack(f'{len(d_data)}f', *d_data))

    return json.dumps({
        'user_id': user.user_id,
        'user_name': user.user_name,
        'birth': user.birth,
        'gender': user.gender,
        'feelings': snapshot.feelings,
        'timestamp': snapshot.timestamp,
        'rotation': snapshot.rotation,
        'translation': snapshot.translation,
        'color_image': [w, h, raw_color_path, color_path],
        'depth_image': [d_w, d_h, raw_depth_path, depth_path]})


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
            to_publish = dump_snapshot(hello.user, snapshot)
            self.publish(to_publish)
        finally:
            Handler.lock.release()


def run_server(host: str, port: int, publish=print):
    with Listener(port, host=host) as listener:
        print(f'Listening on {host}:{port}')
        while True:
            connection = listener.accept()
            print('I got connection. handling...')
            handler = Handler(connection, publish)
            handler.start()
