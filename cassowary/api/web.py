from flask import Flask

app = Flask(__name__)

NO_SUCH_USER = 'The specified user is not found'
NO_SUCH_SNAPSHOT = 'The specified snapshot is not found'
NO_SUCH_SNAPSHOT_RESULT = 'The specified snapshot result is not found'


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
            return '', 404
        user_snapshots = db.get_user_snapshots(user_id)
        return user_snapshots, 200

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
    def get_user_snapshot(user_id, snapshot_id):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return NO_SUCH_SNAPSHOT, 404
        return snapshot, 200

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
    def get_user_snapshot(user_id, snapshot_id, result_name):
        user = db.get_user(user_id)
        if user is None:
            return NO_SUCH_USER, 404
        snapshot = db.get_user_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return NO_SUCH_SNAPSHOT, 404
        if result_name not in snapshot:
            return NO_SUCH_SNAPSHOT_RESULT, 404
        return snapshot[result_name], 200

