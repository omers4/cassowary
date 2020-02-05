from .parsers import Parsers


def run_parser(parser_name: str, data: dict) -> dict:
    """
    :param parser_name: the name of the parser we want to parse i's data
    :param data: the data, as received from the message queue
    :return: the parsed data, as sent to the message queue
    """
    Parsers.load_parsers()
    parser = Parsers.parsers[parser_name]()
    return parser.parse(data)
