import click
from . import Saver


@click.command('save')
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017', help='DB hostname / IP')
@click.argument('parser_name')
@click.argument('raw_data_path')
def save_command(database: str, parser_name: str, raw_data_path: str):
    pass


@click.command('run-saver')
@click.argument('db_path')
def run_save_command(db_path: str):
    pass
