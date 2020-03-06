import os
from typing import Callable


class Parsers:
    """
    This class aims to collect all given parsers by their name and directory.
    """
    parsers = {}

    @staticmethod
    def load_parsers():
        """
        We load every python module which ends with _parser.py,
        For example: pose_parser.py.
        """
        files = os.listdir(os.path.dirname(__file__))
        for module_name in files:
            if module_name.endswith(
                    '_parser.py') and not module_name == 'base_parser.py':
                __import__(module_name[:-3], globals(), locals(), [], 1)

    @staticmethod
    def parser(name: str) -> Callable:
        """
        This decorator is used to decorate parser classes,
        in order to tell the infrastructure they need to be collected.
        """

        def decorator(cls):
            Parsers.parsers[name] = cls
            return cls

        return decorator


parser = Parsers.parser


def run_parser(parser_name: str, data: dict) -> dict:
    """
    :param parser_name: the name of the parser we want to parse i's data
    :param data: the data, as received from the message queue
    :return: the parsed data, as sent to the message queue
    """
    Parsers.load_parsers()
    return Parsers.parsers[parser_name]().parse(data)
