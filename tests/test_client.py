import socket
import time

import pytest
from click.testing import CliRunner
from cassowary.client.__main__ import upload_sample_command


# @pytest.fixture
# def server():
#     server = socket.socket()
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server.bind(('0.0.0.0', 8000))
#     server.listen(1000)
#     try:
#         time.sleep(0.1)
#         yield server
#     finally:
#         server.close()

#
# def test_client_cli_sanity(server):
#     runner = CliRunner()
#     result = runner.invoke(upload_sample_command, ['/home/user/Downloads/sample.mind.gz'])
#     assert 'Start uploading the snapshot in my_path to 127.0.0.1:8000' in result.output
#     assert 'Done uploading the snapshot' in result.output
