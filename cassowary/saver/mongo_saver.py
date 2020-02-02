from pymongo import MongoClient


class MongoConnection:
    def __init__(self, database_url):
        self.client = MongoClient(database_url)
        self.db = self.client.snapshots_database
        self.users_col = self.db.users
        self.snapshots_col = self.db.users_snapshots

    @classmethod
    def connect(cls, database_url):
        return MongoConnection(database_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def save_user(self, data):
        self.users_col.update({'user_id': data['user_id']},
                              {'$set': data['personal_details']},
                              upsert=True)

    def save(self, parser_name, data):
        if parser_name == 'personal_details':
            return self.save_user(data)
        self.snapshots_col.update(
            {'user_id': data['user_id'], 'timestamp': data['timestamp']},
            {'$set': {
                'user_id': data['user_id'],
                'timestamp': data['timestamp'],
                parser_name: data[parser_name]
            }}, upsert=True)

