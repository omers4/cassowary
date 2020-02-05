import json
import pika


class BaseParser:
    """
    The target of this class is to represent a parser.
    Each parser has the opportunity to init a message queue and to parse results.
    """
    def __init__(self):
        self.channel = None

    def parse(self, data: dict) -> dict:
        """
        :param data: the data as received from the message queue
        :return: the parsed data to send to the message queue
        """
        raise NotImplementedError()

    def init_message_queue(self, host, port):
        """
        This method initialized a rabbitMQ message queue
        :param host: the host of our mq server
        :param port: the post of our mq server
        """
        print('establishing a message queue...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='parsed-result')

        self.channel.exchange_declare(exchange='raw-snapshot',
                                      exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='raw-snapshot', queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        print('start listening for snapshots...')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """
        This is our MQ callback, responsible for receiving the raw data
        and passing the parsed result to the message queue
        """
        parsed_data = self.parse(json.loads(body))
        print('parsed data: ', parsed_data)
        self.channel.basic_publish(exchange='',
                                   routing_key='parsed-result',
                                   body=json.dumps(parsed_data))
