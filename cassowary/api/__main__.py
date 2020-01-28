import click
from . import run_api_server


@click.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
@click.option('-d', '--database', default='postgresql://127.0.0.1:5432', help='Database hostname / IP')
def run_server_command(host: str, port: int, database: ''):
    run_api_server(host, port, database)
