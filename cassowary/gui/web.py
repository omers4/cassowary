import datetime
import io
import sys
from math import ceil

from ..db.exceptions import DBConnectionException
from ..db.utils import get_database

from flask import Flask, render_template, send_file

app = Flask(__name__)


def register_views(db):
    @app.route('/')
    def get_users_page():
        return render_template('index.html', users=db.get_users())

    @app.route('/users/<int:user_id>')
    def get_user_page(user_id):
        user = db.get_user(user_id)
        birthday = datetime.datetime.fromtimestamp(user['birth'])
        user['age'] = ceil((datetime.datetime.now() - birthday).days / 365)
        if user is None:
            return render_template('404.html')
        snapshots = db.get_user_snapshots_data(user_id)
        for snapshot in snapshots:
            timestamp = snapshot['timestamp']
            snapshot['date'] = datetime.datetime.fromtimestamp(timestamp
                                                               / 1000)
            if snapshot['pose']:
                x, y, z = snapshot['pose']['translation']
                snapshot['x'] = x
                snapshot['y'] = y
                snapshot['z'] = z
        return render_template('user.html', user=user, snapshots=snapshots)

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>'
               '/<result_name>/data')
    def get_user_snapshot_result_image(user_id, snapshot_id, result_name):
        user = db.get_user(user_id)
        if user is None:
            return render_template('404.html')
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return render_template('404.html')
        if result_name not in snapshot['results']:
            return render_template('404.html')
        if 'path' not in snapshot['results'][result_name]:
            return render_template('404.html')

        path = snapshot['results'][result_name]['path']
        with open(path, 'rb') as image:
            return send_file(io.BytesIO(image.read()),
                             mimetype='image/png')


def run_server(host, port, database_url):
    db_cls = get_database(database_url)
    try:
        with db_cls.connect(database_url) as db:
            register_views(db)
            app.run(host, port)
    except DBConnectionException:
        print(f'ERROR connecting to db: {database_url}', file=sys.stderr)
        return 1
    except Exception as error:
        print(f'ERROR running the api server: {error}', file=sys.stderr)
        return 1
