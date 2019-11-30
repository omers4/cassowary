import time
from .cli import CommandLineInterface
from .thought import Thought
from .utils.connection import Connection

cli = CommandLineInterface()


def upload_thought(address, user, thought):
    ip, port = address.split(':')
    with Connection.connect(ip, int(port)) as connection:
        given_thought = Thought(int(user), int(time.time()), thought)
        connection.send(given_thought.serialize())


@cli.command
def upload(address, user, thought):
    try:
        upload_thought(address, user, thought)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
