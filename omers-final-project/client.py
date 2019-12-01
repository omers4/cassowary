import time
from .thought import Thought
from .utils.connection import Connection


def upload_thought(address, user, thought):
    ip, port = address.split(':')
    with Connection.connect(ip, int(port)) as connection:
        given_thought = Thought(int(user), int(time.time()), thought)
        connection.send(given_thought.serialize())
