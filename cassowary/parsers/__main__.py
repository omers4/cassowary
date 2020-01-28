import click
from . import run_parser


@click.command('parse')
@click.argument('parser_name')
@click.argument('raw_data_path')
def parse_command(parser_name: str, raw_data_path: str):
    run_parser(parser_name, {})


@click.command('run-parser')
@click.argument('parser_name')
@click.argument('publish_url')
def run_parser_command(parser_name: str, publish_url: str):
    run_parser(parser_name, publish_url)
