from .web import register_thoughts_views, app


def run_api_server(host, port, database_url):
    db = None
    register_thoughts_views(db)
    app.run(host, port)
