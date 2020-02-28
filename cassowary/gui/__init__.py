from .web import app, register_views
from ..db.utils import get_database


def run_server(host, port, database_url):
    db_cls = get_database(database_url)
    with db_cls.connect(database_url) as db:
        register_views(db)
        app.run(host, port, debug=True)
