import click
from . import run_server


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='0.0.0.0',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8080, type=int,
              help='Port to connect run API server with')
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017',
              help='Database hostname / IP')
def run_server_command(host: str, port: int, database: str):
    run_server(host, port, database)


if __name__ == '__main__':
    cli()
