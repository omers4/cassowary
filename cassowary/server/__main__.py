import click
import furl
import pika

from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('publish_url')
@click.option('-h', '--host', default='0.0.0.0', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Server port')
def run_server_command(publish_url: str, host: str, port: int):
    formatted_publish_url = furl.furl(publish_url)

    def rabbitmq_publish(message):
        pika_params = pika.ConnectionParameters(formatted_publish_url.host,
                                                formatted_publish_url.port)
        connection = pika.BlockingConnection(pika_params)
        channel = connection.channel()
        channel.exchange_declare(exchange='raw-snapshot',
                                 exchange_type='fanout')
        channel.basic_publish(exchange='raw-snapshot',
                              routing_key='server',
                              body=message)

    run_server(host, port, rabbitmq_publish)


if __name__ == '__main__':
    cli()
