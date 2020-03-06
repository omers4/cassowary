from typing import Callable


class HandlerBase:

    @staticmethod
    def connect(host: str, port: int):
        """
        Returns a new message queue handler
        :param host: the host of the server address
        :param port: the port of the server address
        """
        raise NotImplementedError

    def define_queue(self, queue: str):
        """
        Defines a queue for writing or reading
        :param queue: the name of the queue
        """
        raise NotImplementedError

    def define_publish_queue(self, queue: str):
        """
        Defines a publish queue to listen to
        :param queue: the name of the publish queue
        """
        raise NotImplementedError

    def publish_to_queue(self, queue: str, routing_key: str, message: str):
        """
        This method publishes a message to the queue with a routing key
        :param queue: the name of the queue
        :param routing_key: the name of the routing key
        :param message: the message we want to publish
        """
        raise NotImplementedError

    def start_listening_queue(self, queue: str, callback: Callable):
        """
        Starts listening for messages from a queue
        :param queue: the name of the queue
        :param callback: a func to be invoked when a message is received
        """
        raise NotImplementedError

    def bind_queue_to_exchange(self, exchange: str, callback: Callable):
        """
        Similar to start_listening_queue, when the routing is unknown.
        :param exchange: the name of the exchange queue
        :param callback: a func to be invoked when a message is received
        :return:
        """
        raise NotImplementedError
