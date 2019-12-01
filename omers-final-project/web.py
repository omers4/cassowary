import datetime
from flask import Flask
import os

app = Flask(__name__)

USERS = '''<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

USER = '<li><a href="/users/{user_id}">user {user_id}</a></li>'

THOUGHTS = '''<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''

THOUGHT = '<tr><td>{date}</td><td>{thought}</td></tr>'


def get_user_thoughts(user, user_dir):
    user_thoughts_list = []
    dates = os.listdir(user_dir)
    for date in dates:
        with open(f'{user_dir}/{date}', 'r') as thought_file:
            raw_thought = thought_file.read()
            datetime_obj = datetime.datetime.strptime(date,
                                                      '%Y-%m-%d_%H-%M-%S.txt')
            date_as_string = str(datetime_obj)
            user_thoughts_list.append(THOUGHT.format(date=date_as_string,
                                                     thought=raw_thought))
    return user_thoughts_list


def get_users(data_dir):
    users_list = []
    users = os.listdir(data_dir)
    users.sort()
    for user in users:
        users_list.append(USER.format(user_id=user))
    return users_list


def register_thoughts_views(data_dir):
    @app.route('/')
    def users():
        users_list = get_users(data_dir)
        return USERS.format(users=''.join(users_list)), 200

    @app.route('/users/<int:user_id>')
    def user(user_id):
        user_dir = f'{data_dir}/{user_id}'
        if not os.path.exists(user_dir):
            return '', 404
        user_thoughts_list = get_user_thoughts(user_id, user_dir)
        user_thoughts_html = THOUGHTS.format(thoughts=''.join(
            user_thoughts_list),
            user_id=user_id)
        return user_thoughts_html, 200


def run_webserver(address, data_dir):
    register_thoughts_views(data_dir)
    app.run(*address)
