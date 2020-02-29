import datetime
import threading
from time import sleep
from unittest.mock import MagicMock

from cassowary.server import run_server
from cassowary.client import upload_sample
from cassowary.utils.protocol import User


class MockReader:
    def __init__(self, sample_path):
        self.sample_path = sample_path
        self.file = MagicMock()
        self.file.close.return_value = True
        self.counter = 0

    def read_user(self):
        return User(1, 'test', int(datetime.datetime(year=1994, month=5, day=4).timestamp()), 'f')

    def next_snapshot(self):
        raise StopIteration()


def run_test_server():
    run_server('0.0.0.0', 8200)


def test_client_sanity(capsys):
    """
    This system test verifies the basic protocol between the server and the client - hello-config-results.
    """
    server_thread = threading.Thread(target=run_test_server)
    server_thread.daemon = True
    server_thread.start()
    sleep(1)

    output, err = capsys.readouterr()
    assert 'Listening on 0.0.0.0:8200' in output

    upload_sample('0.0.0.0', 8200, '', MockReader)

    output, err = capsys.readouterr()
    assert 'Start uploading the snapshot in  to 0.0.0.0:8200' in output
    assert 'Done uploading the snapshot' in output
