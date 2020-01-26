from click.testing import CliRunner
from cassowary.client.__main__ import upload_sample_command


def test_client_cli_sanity():
    runner = CliRunner()
    result = runner.invoke(upload_sample_command, ['my_path'])
    assert 'Start uploading the snapshot in my_path to 127.0.0.1:8000' in result.output
    assert 'Done uploading the snapshot' in result.output
