import json
import sys
from functools import update_wrapper
import click
from cassowary.mq.message_queues import MessageQueues
from ..db.exceptions import DBConnectionException
from ..mq.exceptions import MQConnectionError, NoSuchMQ
from . import Saver


def wrap_with_conn_error(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        try:
            return ctx.invoke(f, *args, **kwargs)
        except DBConnectionException:
            print('ERROR: Could not connect to db')
        except MQConnectionError as e:
            print(f'ERROR connecting to the given MQ: {e}', file=sys.stderr)
            return 1
        except NoSuchMQ as e:
            print(f'ERROR connecting to the given MQ: {e}', file=sys.stderr)
            return 1
    return update_wrapper(wrapper, f)


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017',
              help='DB hostname / IP')
@click.argument('parser_name')
@click.argument('raw_data_path')
@wrap_with_conn_error
def save_command(database: str, parser_name: str, raw_data_path: str):
    with open(raw_data_path) as data_file:
        data = data_file.read()
        Saver(database).save(parser_name, json.loads(data))


@cli.command('run-saver')
@click.argument('database')
@click.argument('publish_url')
@wrap_with_conn_error
def run_save_command(database: str, publish_url: str):
    MessageQueues.load_mqs()
    Saver(database, publish_url).init_message_queue()


if __name__ == '__main__':
    cli()
