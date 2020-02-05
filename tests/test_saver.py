import os
from time import sleep

from click.testing import CliRunner

from cassowary.saver import Saver
from cassowary.saver.__main__ import save_command


def test_saver(mongodb):
    saver = Saver('mongodb://127.0.0.1:27017')
    saver.save('pose', {'name': 'pose',
                        'user_id': 1, 'timestamp': 1234,
                        'pose': {'translation': {'x': 2, 'y': 3, 'z': 4},
                                 'rotation': {'x': 2, 'y': 3, 'z': 4, 'w': 1}}})
    snapshot = mongodb.users_snapshots.find_one({'user_id': 1})
    assert snapshot is not None
    assert snapshot['pose'] == {'translation': {'x': 2, 'y': 3, 'z': 4},
                                'rotation': {'x': 2, 'y': 3, 'z': 4, 'w': 1}}


def test_save_cli_sanity(mongodb):
    details_path = os.path.join(os.path.dirname(__file__), 'resources', 'parsed_personal_details.txt')
    runner = CliRunner()
    result = runner.invoke(save_command, ['-d', 'mongodb://127.0.0.1:27017', 'personal_details',
                                          details_path])
    assert result.exit_code == 0
    user = mongodb.users.find_one({'user_id': 1})
    assert user is not None
