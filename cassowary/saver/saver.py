import json
from cassowary.db.utils import get_database
from cassowary.mq.message_queues import MessageQueues


class Saver:
    """
    Saver represents an object that manages db connection and saves to db
    """
    def __init__(self, database_url, publish_url=''):
        self.database_url = database_url
        self.publish_url = publish_url
        self.database = get_database(database_url)

    def save(self, parser_name, data):
        """
        Saves parsed data in db according to he given scheme in the url
        :param parser_name: the name of the parser, ie. pose
        :param data: the data as consumed by the message queue
        """
        with self.database.connect(self.database_url) as connection:
            connection.save(parser_name, data)

    def init_message_queue(self):
        print('establish a message queue')
        queue = MessageQueues.get_message_queue(self.publish_url)
        queue.define_queue('parsed-result')
        print('start listening for parsed results...')
        queue.start_listening_queue('parsed-result', self.callback)

    def callback(self, raw_result):
        parsed_result = json.loads(raw_result)
        print('received parsed data', parsed_result)

        parser_name = parsed_result['name']
        self.save(parser_name, parsed_result)
        print(f'saved {parser_name} successfully')
