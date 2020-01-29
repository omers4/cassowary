from click.testing import CliRunner

from cassowary.server.__main__ import run_server_command


# def test_server_cli_sanity():
#     runner = CliRunner()
#     result = runner.invoke(run_server_command, ['rabbitmq://127.0.0.1:5672/'])
#     assert result.exit_code == 0
