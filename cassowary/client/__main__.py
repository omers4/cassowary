import click
from . import upload_sample


@click.command('upload-sample')
@click.option('-h', '--host', default='127.0.0.1', help='Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int, help='Port to connect to server with')
@click.argument('path')
def upload_sample_command(host: str, port: int, path: ''):
    upload_sample(host, port, path)
