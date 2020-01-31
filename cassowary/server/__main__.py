import click
import pika

from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('publish_url')
@click.option('-h', '--host', default='127.0.0.1', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Server port')
def run_server_command(publish_url: str, host: str, port: int):

    def my_publish(message):
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672))
        channel = connection.channel()
        channel.exchange_declare(exchange='raw-snapshot', exchange_type='fanout')
        channel.basic_publish(exchange='raw-snapshot',
                              routing_key='server',
                              body=message)

    run_server(host, port, my_publish)


if __name__ == '__main__':
    cli()
