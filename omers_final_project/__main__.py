import click
from .server import run_server
from .client import upload_snapshot
from .web import run_webserver
from .reader import Reader


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
@click.argument('path')
def upload(address, path):
    try:
        with Reader(path) as reader:
            upload_snapshot(address, reader)
        print('done')
    except Exception as error:
        # print(f'ERROR: {error}')
        raise
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


@cli.command()
@click.argument('path')
def read(path):
    with Reader(path) as reader:
        print(reader)
        for thought in reader.thoughts:
            print(thought)


if __name__ == '__main__':
    cli()
