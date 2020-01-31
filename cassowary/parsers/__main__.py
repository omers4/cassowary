import json

import click
import furl

from . import run_parser
from . import Parsers


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser_name')
@click.argument('raw_data_path')
def parse_command(parser_name: str, raw_data_path: str):
    with open(raw_data_path, 'r') as f:
        result = run_parser(parser_name, json.loads(f.read()))
        print(result)


@cli.command('run-parser')
@click.argument('parser_name')
@click.argument('publish_url')
def run_parser_command(parser_name: str, publish_url: str):
    formatted_publish_url = furl.furl(publish_url)
    Parsers.load_parsers()
    parser = Parsers.parsers[parser_name]()
    parser.init_message_queue(formatted_publish_url.host, formatted_publish_url.port)


if __name__ == '__main__':
    cli()
