import os


class Parsers:
    parsers = {}

    @staticmethod
    def load_parsers():
        files = os.listdir(os.path.dirname(__file__))
        for module_name in files:
            if module_name.endswith('_parser.py') and not module_name == 'base_parser.py':
                __import__(module_name[:-3], globals(), locals(), [], 1)

    @staticmethod
    def parser(name):

        def decorator(cls):
            Parsers.parsers[name] = cls
            return cls

        return decorator


parser = Parsers.parser
