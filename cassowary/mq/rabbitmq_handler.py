from typing import Callable

import pika
from pika.exceptions import AMQPConnectionError

from .handler_base import HandlerBase
from .exceptions import MQConnectionError
from .message_queues import MessageQueues


@MessageQueues.message_queue('rabbitmq')
class RabbitMQHandler(HandlerBase):
    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

    @staticmethod
    def connect(host, port):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host, port))
            channel = connection.channel()
            return RabbitMQHandler(connection, channel)
        except AMQPConnectionError as e:
            raise MQConnectionError(f'Cant connect to {host}:{port}. {e}')

    def define_queue(self, queue):
        self.channel.queue_declare(queue=queue)

    def define_publish_queue(self, queue):
        self.channel.exchange_declare(exchange=queue,
                                      exchange_type='fanout')

    def bind_queue_to_exchange(self, exchange: str, callback: Callable):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(queue=queue_name,
                                   on_message_callback=self._wrapper(callback),
                                   auto_ack=True)
        self.channel.start_consuming()

    def start_listening_queue(self, queue: str, callback: Callable):
        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self._wrapper(callback),
                                   auto_ack=True)
        self.channel.start_consuming()

    @staticmethod
    def _wrapper(callback: Callable):
        def func(ch, method, properties, body):
            callback(body)
        return func

    def publish_to_queue(self, queue: str, routing_key: str, message: str):
        self.channel.basic_publish(exchange=queue,
                                   routing_key=routing_key,
                                   body=message)
