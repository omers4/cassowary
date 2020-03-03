import datetime
import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='127.0.0.1',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect API server with')
def get_users(host: str, port: int):
    """
    Invoke: $ python -m cassowary.cli get-users
    :param host: API Server hostname / IP
    :param port: Port to connect API server with
    """
    response = requests.get(f'http://{host}:{port}/users')
    users = response.json()['users']
    if users:
        print(f'Users found ({len(users)}):')
        for user in users:
            print(f"Name: {user['user_name']} ({user['user_id']})")
    else:
        print('No users were found.')


@cli.command()
@click.option('-h', '--host', default='127.0.0.1',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect run API server with')
@click.argument('user_id', type=int)
def get_user(host: str, port: int, user_id: int):
    """
    Invoke: python -m cassowary.cli get-user 1
    :param user_id: the id of the user
    :param host: API Server hostname / IP
    :param port: Port to connect API server with
    """
    response = requests.get(f'http://{host}:{port}/users/{user_id}')
    if response.status_code == requests.codes.ok:
        user = response.json()
        print(f"ID: {user['user_id']}")
        print(f"Name: {user['user_name']}")
        birth = datetime.datetime.fromtimestamp(user['birth']/1000)
        print(f"Birth: {birth}")
        print(f"Gender: {'male' if user['gender'] == 'm' else 'female'}")
    elif response.status_code == requests.codes.not_found:
        print(response.text)


@cli.command()
@click.option('-h', '--host', default='127.0.0.1',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect run API server with')
@click.argument('user_id', type=int)
def get_snapshots(host: str, port: int, user_id: int):
    """
    Invoke: python -m cassowary.cli get-snapshots 1
    :param user_id: the id of the user
    :param host: API Server hostname / IP
    :param port: Port to connect API server with
    """
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
    if response.status_code == requests.codes.ok:
        snapshots = response.json()['snapshots']
        if snapshots:
            print(f'Snapshots found ({len(snapshots)} total):')
            for snapshot in snapshots:
                print(f"ID: {snapshot['id']}, Date: {snapshot['date']}")
        else:
            print('No snapshots were found.')
    elif response.status_code == requests.codes.not_found:
        print(response.text)


@cli.command()
@click.option('-h', '--host', default='127.0.0.1',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect run API server with')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def get_snapshot(host: str, port: int, user_id: int, snapshot_id: int):
    """
    Invoke: $ python -m cassowary.cli get-snapshot 1 2
    :param user_id: the id of the user
    :param snapshot_id: the id of the snapshot
    :param host: API Server hostname / IP
    :param port: Port to connect API server with
    """
    response = requests.get(f'http://{host}:{port}/users/{user_id}/'
                            f'snapshots/{snapshot_id}')
    if response.status_code == requests.codes.ok:
        snapshot = response.json()
        print(f"ID: {snapshot['id']}")
        print(f"Date: {snapshot['date']}")
        print(f"Results: {snapshot['results']}")
    elif response.status_code == requests.codes.not_found:
        print(response.text)


@cli.command()
@click.option('-h', '--host', default='127.0.0.1',
              help='API Server hostname / IP')
@click.option('-p', '--port', default=8000, type=int,
              help='Port to connect run API server with')
@click.option('-s', '--save', help='Path to save the result')
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('parser_name')
def get_result(host: str, port: int, save: str, user_id: int,
               snapshot_id: int, parser_name: str):
    """
    Invoke: $ python -m cassowary.cli get-result 1 2 'pose'
    :param user_id: the id of the user
    :param save: path to save the results in
    :param parser_name: the name of the parser
    :param snapshot_id: the id of the snapshot
    :param host: API Server hostname / IP
    :param port: Port to connect API server with
    """
    response = requests.get(f'http://{host}:{port}/users/{user_id}/'
                            f'snapshots/{snapshot_id}/{parser_name}')
    if response.status_code == requests.codes.ok:
        print(f"Results for {parser_name}:")
        print(response.text)
        if save:
            print(f'Saving the data to {save}...')
            with open(save, 'w') as output:
                output.write(response.text)
            print('Done.')
    elif response.status_code == requests.codes.not_found:
        print(response.text)


if __name__ == '__main__':
    cli()
