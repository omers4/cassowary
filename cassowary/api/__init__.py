from ..db.utils import get_database
from .web import register_thoughts_views, app


def run_api_server(host, port, database_url):
    db_cls = get_database(database_url)
    with db_cls.connect(database_url) as db:
        register_thoughts_views(db)
        app.run(host, port)
