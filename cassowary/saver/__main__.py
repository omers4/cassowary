import json

import click
import furl

from . import Saver


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017', help='DB hostname / IP')
@click.argument('parser_name')
@click.argument('raw_data_path')
def save_command(database: str, parser_name: str, raw_data_path: str):
    with open(raw_data_path) as data_file:
        data = data_file.read()
        Saver(database).save(parser_name, json.loads(data))


@cli.command('run-saver')
@click.argument('database')
@click.argument('publish_url')
def run_save_command(database: str, publish_url: str):
    formatted_publish_url = furl.furl(publish_url)
    Saver(database).init_message_queue(formatted_publish_url.host, formatted_publish_url.port)


if __name__ == '__main__':
    cli()
