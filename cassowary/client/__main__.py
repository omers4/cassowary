import click
from . import upload_sample


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', default='0.0.0.0', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect to server with')
@click.argument('path')
def upload_sample_command(host: str, port: int, path=''):
    upload_sample(host, port, path)


if __name__ == '__main__':
    cli()
