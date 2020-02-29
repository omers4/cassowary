import furl
from .mongo_connection import MongoConnection

databases = {
    'mongodb': MongoConnection
}


def get_database(database_url: str):
    """
    This method returns a database connection based on the scheme of the url.
    I could use aspect oriented, but it's too much overhead at this point,
    since we only have one db practically.
    One can easily extend this by adding more connections to databases dictionary.
    :param database_url: the url of the database
    :return: the database connection
    """
    formatted_database_url = furl.furl(database_url)
    db_type = formatted_database_url.scheme
    return databases[db_type]
