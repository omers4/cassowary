import json
import furl
import pika

from cassowary.saver.mongo_saver import MongoConnection

savers = {
    'mongodb': MongoConnection
}


class Saver:
    def __init__(self, database_url):
        formatted_database_url = furl.furl(database_url)
        db_type = formatted_database_url.scheme
        db_connection_cls = savers[db_type]
        self.database_url = database_url
        self.connection = db_connection_cls

    def save(self, parser_name, data):
        with self.connection.connect(self.database_url) as connection:
            connection.save(parser_name, data)

    def init_message_queue(self, host, port):
        print('establish a message queue')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='parsed-result')
        self.channel.basic_consume(queue='parsed-result', on_message_callback=self.callback, auto_ack=True)
        print('start listening for parsed results...')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        parsed_result = json.loads(body)
        parser_name = parsed_result['name']
        print('received parsed data', parsed_result)
        self.save(parser_name, parsed_result)
        print(f'saved {parser_name} successfully')
