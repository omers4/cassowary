import click
from .server import run_server
from .client import upload_snapshot
from .web import run_webserver
from .reader import Reader
from .file_readers.binary_reader import BinaryReader
from .file_readers.protobuff_reader import ProtobuffReader


@click.group()
def cli():
    pass


@cli.group('web')
def web():
    pass


@cli.group('server')
def server():
    pass


@cli.group('client')
def client():
    pass


@server.command()
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


@client.command()
@click.argument('address')
@click.argument('path')
@click.argument('version')
def upload(address, path, version):
    try:
        reader = BinaryReader if version == 'v1' else ProtobuffReader
        print(f'parsing the file using version {version}')
        with Reader(path, reader) as reader:
            upload_snapshot(address, reader)
        print('done')
    except Exception as error:
        # print(f'ERROR: {error}')
        raise
        return 1


@web.command()
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


@client.command()
@click.argument('path')
@click.argument('version')
def read(path, version):
    reader = BinaryReader if version == 'v1' else ProtobuffReader
    print(f'parsing the file using version {version}')
    with Reader(path, reader) as reader:
        print(reader.user)
        for thought in reader.thoughts:
            print(thought)


if __name__ == '__main__':
    cli()
