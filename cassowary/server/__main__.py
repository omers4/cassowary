import click
from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('publish_url')
@click.option('-h', '--host', default='127.0.0.1', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Server port')
def run_server_command(publish_url: str, host: str, port: int):
    print('Hi?')
    print(publish_url)
    def my_publish(message):
        print(message + publish_url)
    run_server(host, port, my_publish)


if __name__ == '__main__':
    cli()
