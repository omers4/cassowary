import os
from typing import Callable

import furl

from .exceptions import NoSuchMQ
from .handler_base import HandlerBase


class MessageQueues:
    """
    This class aims to collect all given message queues by their
    name and directory.
    """
    message_queues = {}

    @staticmethod
    def load_mqs():
        """
        We load every python module which ends with _handler.py,
        For example: pose_parser.py.
        """
        files = os.listdir(os.path.dirname(__file__))
        for module_name in files:
            if module_name.endswith('_handler.py'):
                __import__(module_name[:-3], globals(), locals(), [], 1)

    @staticmethod
    def message_queue(name: str) -> Callable:
        """
        This decorator is used to decorate message queue classes,
        in order to tell the infrastructure they need to be collected.
        """
        def decorator(cls):
            MessageQueues.message_queues[name] = cls
            return cls

        return decorator

    @staticmethod
    def get_message_queue(publish_url: str) -> HandlerBase:
        formatted_database_url = furl.furl(publish_url)
        db_type = formatted_database_url.scheme
        if db_type not in MessageQueues.message_queues:
            raise NoSuchMQ(f'The only supported mqs are: '
                           f'{list(MessageQueues.message_queues.keys())}')
        return MessageQueues.message_queues[db_type].connect(
            formatted_database_url.host,
            formatted_database_url.port)
