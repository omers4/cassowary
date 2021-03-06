import io
import os
import sys

from ..db.exceptions import DBConnectionException
from ..db.utils import get_database
from flask import Flask, send_file

app = Flask(__name__)

NO_SUCH_USER = 'The specified user is not found'
NO_SUCH_SNAPSHOT = 'The specified snapshot is not found'
NO_SUCH_SNAPSHOT_RESULT = 'The specified snapshot result is not found'
NO_FURTHER_DATA = 'The specified snapshot result doesnt have image'


def register_thoughts_views(db):
    @app.route('/users')
    def get_users():
        users_list = db.get_users()
        return {'users': users_list}, 200

    @app.route('/users/<int:user_id>')
    def get_user(user_id):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        return user, 200

    @app.route('/users/<int:user_id>/snapshots')
    def get_user_snapshots(user_id):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        user_snapshots = db.get_user_snapshots_ids(user_id)
        return {'snapshots': user_snapshots}, 200

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
    def get_user_snapshot(user_id, snapshot_id):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return NO_SUCH_SNAPSHOT, 404
        snapshot['results'] = list(snapshot['results'].keys())
        return snapshot, 200

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/'
               '<result_name>')
    def get_user_snapshot_result(user_id, snapshot_id, result_name):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return NO_SUCH_SNAPSHOT, 404
        if result_name not in snapshot['results']:
            return NO_SUCH_SNAPSHOT_RESULT, 404
        result = snapshot['results'][result_name]
        if 'path' in result:
            result['data'] = f'/users/{user_id}/snapshots/{snapshot_id}/' \
                             f'{result_name}/data'
        return snapshot['results'][result_name], 200

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/'
               '<result_name>/data')
    def get_user_snapshot_result_image(user_id, snapshot_id, result_name):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return NO_SUCH_SNAPSHOT, 404
        if result_name not in snapshot['results']:
            return NO_SUCH_SNAPSHOT_RESULT, 404
        if 'path' not in snapshot['results'][result_name]:
            return NO_FURTHER_DATA, 404

        path = snapshot['results'][result_name]['path']
        if not os.path.exists(path):
            return NO_SUCH_SNAPSHOT_RESULT, 404

        with open(path, 'rb') as image:
            return send_file(io.BytesIO(image.read()),
                             mimetype='image/png')


def run_api_server(host: str, port: int, database_url: str):
    """
    runs the flask api server
    :param host: api server address
    :param port: api server port
    :param database_url: the url of the db (mongodb://127.0.0.1:27017)
    """
    db_cls = get_database(database_url)
    try:
        with db_cls.connect(database_url) as db:
            register_thoughts_views(db)
            app.run(host, port)
    except DBConnectionException:
        print(f'ERROR connecting to db: {database_url}', file=sys.stderr)
        return 1
    except Exception as error:
        print(f'ERROR running the api server: {error}', file=sys.stderr)
        return 1
