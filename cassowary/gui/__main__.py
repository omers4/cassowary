import click
from . import run_server


@click.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='GUI hostname / IP')
@click.option('-p', '--port', default=8080, type=int, help='Port to connect run GUI with')
@click.option('-H', '--api-host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-P', '--api-port', default=5000, type=int, help='Port to connect run API server with')
def run_server_command(host: str, port: int, api_host: str, api_port: int):
    run_server(host, port, api_host, api_port)
