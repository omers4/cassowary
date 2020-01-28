from click.testing import CliRunner

from cassowary.parsers.__main__ import run_parser_command, parse_command


def test_parse_sanity():
    runner = CliRunner()
    result = runner.invoke(parse_command, ['pose', 'raw.data'])
    assert result.exit_code == 0


def test_run_parser_sanity():
    runner = CliRunner()
    result = runner.invoke(run_parser_command, ['pose', 'rabbitmq://127.0.0.1:5672/'])
    assert result.exit_code == 0
