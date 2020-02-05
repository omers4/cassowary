import os

import pytest
from click.testing import CliRunner

from cassowary.parsers import run_parser, Parsers
from cassowary.parsers.__main__ import parse_command

resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
raw_snapshot_file_path = os.path.join(resources_dir, 'snapshot_raw.txt')

expected_cli_result_pose = {'name': 'pose', 'user_id': 1, 'timestamp': 1234,
                            'pose': {'translation': {'x': 2, 'y': 3, 'z': 4},
                                     'rotation': {'x': 2, 'y': 3, 'z': 4, 'w': 1}}}
expected_result_feelings = {'name': 'feelings', 'user_id': 1, 'timestamp': 1234,
                            'feelings': {'hunger': 0, 'thirst': 10, 'exhaustion': 2, 'happiness': 3}}
expected_personal_details_feelings = {
    'name': 'personal_details',
    'user_id': 1,
    'personal_details': {
        'user_id': 1,
        'user_name': 'Omer',
        'birth': 45,
        'gender': 'f'
    }
}


@pytest.fixture
def raw_snapshot():
    return {"name": "pose",
            "user_id": 1,
            "user_name": "Omer",
            'birth': 45,
            'gender': 'f',
            "timestamp": 1234,
            "feelings": [0, 10, 2, 3],
            "translation": {"x": 2, "y": 3, "z": 4}, "rotation": {"x": 2, "y": 3, "z": 4, "w": 1} }


def test_parse_pose_cli_sanity():
    runner = CliRunner()
    result = runner.invoke(parse_command, ['pose', raw_snapshot_file_path])
    output = eval(result.stdout_bytes)
    assert output == expected_cli_result_pose
    assert result.exit_code == 0


def test_run_parser_feelings(raw_snapshot):
    result = run_parser('feelings', raw_snapshot)
    assert result == expected_result_feelings


def test_run_parser_personal_details(raw_snapshot):
    result = run_parser('personal_details', raw_snapshot)
    assert result == expected_personal_details_feelings


def test_load_parsers():
    Parsers.load_parsers()
    parsers = Parsers.parsers
    for parser_name in ['pose', 'feelings', 'depth_image', 'depth_image']:
        assert parser_name in parsers
