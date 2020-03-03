import sys

from ..db.utils import get_database
from .web import register_thoughts_views, app


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
    except Exception as error:
        print(f'ERROR running the api server: {error}', file=sys.stderr)
        return 1
