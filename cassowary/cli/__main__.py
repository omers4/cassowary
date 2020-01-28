import click

'''
$ python -m cassowary.cli get-users
…
$ python -m cassowary.cli get-user 1
…
$ python -m cassowary.cli get-snapshots 1
…
$ python -m cassowary.cli get-snapshot 1 2
…
$ python -m cassowary.cli get-result 1 2 'pose'
'''


@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
def get_users(host: str, port: int):
    pass


@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
@click.argument('user_id', type=int)
def get_user(host: str, port: int, user_id: int):
    pass


@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
@click.argument('user_id', type=int)
def get_snapshots(host: str, port: int, user_id: int):
    pass


@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def get_snapshot(host: str, port: int, user_id: int, snapshot_id: int):
    pass


@click.option('-h', '--host', default='127.0.0.1', help='API Server hostname / IP')
@click.option('-p', '--port', default=5000, type=int, help='Port to connect run API server with')
@click.option('-s', '--save', help='Path to save the result')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('parser_name')
def get_result(host: str, port: int, save: str, user_id: int, snapshot_id: int, parser_name: str):
    pass
