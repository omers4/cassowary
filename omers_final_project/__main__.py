import click
from .server import run_server
from .client import upload_thought
from .web import run_webserver


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
@click.argument('data')
def run(address, data):
    try:
        ip, port = address.split(':')
        run_server((ip, int(port)), data)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@cli.command()
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload(address, user, thought):
    try:
        upload_thought(address, user, thought)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@cli.command()
@click.argument('address')
@click.argument('data')
def run_web_server(address, data):
    try:
        ip, port = address.split(':')
        run_webserver((ip, int(port)), data)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli()
