from .parsers import Parsers


def run_parser(parser_name, data):
    Parsers.load_parsers()
    parser = Parsers.parsers[parser_name]()
    return parser.parse(data)
