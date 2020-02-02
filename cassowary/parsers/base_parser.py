import json
import pika


class BaseParser:
    def __init__(self):
        self.channel = None

    def parse(self, data):
        raise NotImplementedError()

    def init_message_queue(self, host, port):
        print('establish a message queue')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='parsed-result')

        self.channel.exchange_declare(exchange='raw-snapshot',
                                      exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='raw-snapshot', queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        print('start listening for snapshots')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        parsed_data = self.parse(json.loads(body))
        print('parsed data', parsed_data)
        self.channel.basic_publish(exchange='',
                                   routing_key='parsed-result',
                                   body=json.dumps(parsed_data))