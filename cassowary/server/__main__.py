import click

from . import run_server


@click.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Server port')
@click.argument('publish_url')
def run_server_command(host: str, port: int, publish_url: str):
    def my_publish(message):
        print(message + publish_url)
    run_server(host, port, my_publish)
