import json
import pika

from cassowary.db.utils import get_database


class Saver:
    """
    Saver represents an object that manages db connection and saves to db
    """
    def __init__(self, database_url):
        self.database_url = database_url
        self.database = get_database(database_url)

    def save(self, parser_name, data):
        """
        Saves parsed data in db according to he given scheme in the url
        :param parser_name: the name of the parser, ie. pose
        :param data: the data as consumed by the message queue
        """
        with self.database.connect(self.database_url) as connection:
            connection.save(parser_name, data)

    def init_message_queue(self, host, port):
        print('establish a message queue')

        connection = pika.BlockingConnection(pika.ConnectionParameters(host,
                                                                       port))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='parsed-result')
        self.channel.basic_consume(queue='parsed-result',
                                   on_message_callback=self.callback,
                                   auto_ack=True)

        print('start listening for parsed results...')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        parsed_result = json.loads(body)
        print('received parsed data', parsed_result)

        parser_name = parsed_result['name']
        self.save(parser_name, parsed_result)
        print(f'saved {parser_name} successfully')
