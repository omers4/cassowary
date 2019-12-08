from .utils.connection import Connection
from .reader import Reader
from .utils.protocol import Hello, Config


def upload_snapshot(address: str, reader: Reader):
    """
    This function receives thought details and server address and
    sends the thought to the server

    :param reader: the reader object used for reaching different fields of the snapshot
    :param address: the server's address for example: 127.0.0.1:8888x
    """
    ip, port = address.split(':')
    for thought in reader.thoughts:
        with Connection.connect(ip, int(port)) as connection:
            print(reader)
            hello = Hello(reader.user_id, reader.user_name, reader.birth, reader.gender)
            print(hello)
            connection.send(hello.serialize())
            config = Config.deserialize(connection.receive())
            print(config)
            print(thought)
            connection.send(thought.serialize(config.fields))
        # given_thought = Thought(int(user), int(time.time()), thought)
        # connection.send(given_thought.serialize())
