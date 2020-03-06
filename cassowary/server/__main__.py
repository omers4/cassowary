import sys
import click

from ..mq.message_queues import MessageQueues
from ..mq.exceptions import MQConnectionError, NoSuchMQ

from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('publish_url')
@click.option('-h', '--host', default='0.0.0.0', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Server port')
def run_server_command(publish_url: str, host: str, port: int):

    def rabbitmq_publish(message):
        MessageQueues.load_mqs()
        try:
            queue = MessageQueues.get_message_queue(publish_url)
        except MQConnectionError as e:
            print(f'ERROR connecting to the given MQ: {e}', file=sys.stderr)
            return 1
        except NoSuchMQ as e:
            print(f'ERROR connecting to the given MQ: {e}', file=sys.stderr)
            return 1
        queue.define_publish_queue('raw-snapshot')
        queue.publish_to_queue('raw-snapshot', 'server', message)

    run_server(host, port, rabbitmq_publish)


if __name__ == '__main__':
    cli()
