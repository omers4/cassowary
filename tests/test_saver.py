from click.testing import CliRunner

from cassowary.saver.__main__ import save_command, run_save_command


def test_save_cli_sanity():
    runner = CliRunner()
    result = runner.invoke(save_command, ['-d', 'mongodb://127.0.0.1:27017', 'pose', 'tests/resources/snapshot_raw.txt'])
    assert result.exit_code == 0

#
# def test_run_saver_cli_sanity():
#     runner = CliRunner()
#     result = runner.invoke(run_save_command, ['mongodb://127.0.0.1:27017'])
#     assert result.exit_code == 0