import datetime
import os
import struct
import threading

from .cli import CommandLineInterface
from .utils.listener import Listener
from .thought import Thought

FORMAT = 'LLI'
PACK_SIZE = struct.calcsize('LLI')

cli = CommandLineInterface()


def save_user_data(thought_obj, data_dir):
    date_repr = str(datetime.datetime.fromtimestamp(thought_obj.timestamp)).replace(' ', '_').replace(':', '-')
    filepath = f'{data_dir}/{thought_obj.user_id}/{date_repr}.txt'
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    add_space = os.path.exists(filepath)
    with open(filepath, 'a') as f:
        if add_space:
            f.write('\n')
        f.write(thought_obj.thought)


lock = threading.Lock()


class Handler(threading.Thread):
    def __init__(self, connection, data_dir):
        super(Handler, self).__init__()
        self.connection = connection
        self.data_dir = data_dir
    
    def run(self):
        with self.connection as connection:
            metadata = connection.receive(PACK_SIZE)
            _, _, thought_size = struct.unpack(FORMAT, metadata)
            raw_thought = connection.receive(thought_size)
        thought_obj = Thought.deserialize(metadata + raw_thought)
        lock.acquire()
        try:
            save_user_data(thought_obj, self.data_dir)
        finally:
            lock.release()


def run_server(address, data_dir):
    ip, port = address
    with Listener(port, host=ip) as listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, data_dir)
            handler.start()


@cli.command
def run(address, data):
    try:
        ip, port = address.split(':')
        run_server((ip, int(port)), data)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
