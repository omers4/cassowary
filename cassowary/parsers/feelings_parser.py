from .parsers import parser
from .base_parser import BaseParser


@parser('feelings')
class FeelingsParser(BaseParser):
    def parse(self, data):
        hunger, thirst, exhaustion, happiness = data['feelings']
        result = dict(
            id=data['user_id'],
            timestamp=data['timestamp'],
            hunger=hunger,
            thirst=thirst,
            exhaustion=exhaustion,
            happiness=happiness
        )
        return result
