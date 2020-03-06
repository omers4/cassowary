import json
from functools import update_wrapper

import click

from ..mq.exceptions import MQConnectionError
from . import run_parser
from . import Parsers


def wrap_with_conn_error(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        try:
            return ctx.invoke(f, *args, **kwargs)
        except MQConnectionError as e:
            print(f'ERROR: Cannot connect to given MQ. {e}')
    return update_wrapper(wrapper, f)


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser_name')
@click.argument('raw_data_path')
@wrap_with_conn_error
def parse_command(parser_name: str, raw_data_path: str):
    with open(raw_data_path, 'r') as f:
        result = run_parser(parser_name, json.loads(f.read()))
        print(result)


@cli.command('run-parser')
@click.argument('parser_name')
@click.argument('publish_url')
@wrap_with_conn_error
def run_parser_command(parser_name: str, publish_url: str):
    Parsers.load_parsers()
    parser = Parsers.parsers[parser_name]()
    parser.init_message_queue(publish_url)


if __name__ == '__main__':
    cli()
