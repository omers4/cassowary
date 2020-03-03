import sys
from ..utils.connection import Connection
from ..snapshot_readers.protobuff_reader import ProtobuffReader
from ..snapshot_readers.snapshot_file import SnapshotFile
from ..utils.protocol import Hello, Config


def upload_sample(host: str, port: int, path: str, reader=ProtobuffReader):
    """
    :param host: the hostname / IP of the server
    :param port: the port of the server
    :param path: the path to the raw snapshot
    :param reader: the reader object used for reaching
    different fields of the snapshot
    """
    try:
        print(f'Start uploading the snapshot in {path} to {host}:{port}')
        with SnapshotFile(path, reader) as snapshot_file:
            print(snapshot_file.user)
            for thought in snapshot_file.thoughts:
                with Connection.connect(host, port) as connection:
                    print('connected!')
                    hello = Hello(snapshot_file.user)
                    connection.send(hello.serialize())
                    config = Config.deserialize(connection.receive())
                    print(config)
                    connection.send(thought.serialize(config.fields))
        print('Done uploading the snapshot')
    except Exception as error:
        print(f'ERROR uploading the snapshot: {error}', file=sys.stderr)
        return 1
