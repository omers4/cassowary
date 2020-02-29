import datetime
from typing import Optional

from pymongo import MongoClient


class MongoConnection:
    def __init__(self, database_url):
        self.client = MongoClient(database_url)
        self.db = self.client.snapshots_database
        self.users_col = self.db.users
        self.snapshots_col = self.db.users_snapshots

    @classmethod
    def connect(cls, database_url: str) -> object:
        """
        Connects to mongo by the given database url
        :param database_url: url to database
        :return: a new mongo connection
        """
        return MongoConnection(database_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def save_user(self, data):
        """
        Saves user data in mongo
        :param data: the data as consumed by the message queue
        """
        self.users_col.update_one({'user_id': data['user_id']},
                                  {'$set': data['personal_details']},
                                  upsert=True)

    def save(self, parser_name, data):
        """
        Saves parsed data in mongo
        :param parser_name: the name of the parser, ie. pose
        :param data: the data as consumed by the message queue
        """
        if parser_name == 'personal_details':
            return self.save_user(data)
        self.snapshots_col.update_one(
            {'user_id': data['user_id'], 'timestamp': data['timestamp']},
            {'$set': {
                'user_id': data['user_id'],
                'timestamp': data['timestamp'],
                parser_name: data[parser_name]
            }}, upsert=True)

    def get_users(self) -> list:
        """
        :return: the list of the current users, each of them in the format {user_id, user_name}
        """
        users_cursor = self.users_col.find({},
                                           {'user_id': 1, 'user_name': 1, '_id': 0})
        return list(users_cursor)

    def get_user(self, user_id: int) -> Optional[dict]:
        return self.users_col.find_one({'user_id': user_id}, {'_id': 0})

    def get_user_snapshots_ids(self, user_id: int) -> list:
        """
        This method returns metadata of a user's snapshots
        :param user_id: the id of the user
        :return: the user snapshot, in the format {id, date}
        """
        snapshots_cursor = self.snapshots_col.find({'user_id': user_id},
                                                   {'_id': 0, 'timestamp': 1})
        snapshots = [{'id': snapshot['timestamp'],
                      'date': datetime.datetime.fromtimestamp(snapshot['timestamp']/1000)}
                     for snapshot in snapshots_cursor]
        return snapshots

    def get_user_snapshots_data(self, user_id: int) -> list:
        """
        This method returns metadata of a user's snapshots
        :param user_id: the id of the user
        :return: the user snapshot, in the format {id, date}
        """
        snapshots_cursor = self.snapshots_col.find({'user_id': user_id},
                                                   {'_id': 0})
        return list(snapshots_cursor)

    def get_user_snapshot(self, user_id: int, snapshot_id: int) -> Optional[dict]:
        """
        This method returns metadata of a specific snapshot
        :param user_id: the id of the user
        :param snapshot_id: the id of the snapshot (timestamp)
        :return: the user snapshot, in the format {id, date, result: []}
        """
        snapshot_results = self.snapshots_col.find_one({'user_id': user_id, 'timestamp': snapshot_id},
                                                       {'_id': 0, 'user_id': 0, 'timestamp': 0})
        if not snapshot_results:
            return

        return {
            'id': snapshot_id,
            'date': datetime.datetime.fromtimestamp(snapshot_id/1000),
            'results': snapshot_results
        }
