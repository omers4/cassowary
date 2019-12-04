import time
from .thought import Thought
from .utils.connection import Connection


def upload_thought(address, user, thought):
    """
    This function receives thought details and server address and
    sends the thought to the server

    :param address: the server's address, for example: 127.0.0.1:8888
    :param user: the user id (number)
    :type user: str or int
    :param thought: the content of the thought
    :type thought: str
    """
    ip, port = address.split(':')
    with Connection.connect(ip, int(port)) as connection:
        given_thought = Thought(int(user), int(time.time()), thought)
        connection.send(given_thought.serialize())
