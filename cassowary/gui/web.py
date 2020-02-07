from flask import Flask, render_template

app = Flask(__name__)


def register_views(db):
    @app.route('/')
    def get_users_page():
        return render_template('index.html', users=db.get_users())

    @app.route('/users/<int:user_id>')
    def get_user_page(user_id):
        user = db.get_user(user_id)
        if user is None:
            return render_template('404.html')
        snapshots = db.get_user_snapshots_ids(user_id)
        return render_template('index.html', user=user, snapshots=snapshots)
