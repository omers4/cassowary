from .parsers import parser
from .base_parser import BaseParser


@parser('feelings')
class FeelingsParser(BaseParser):
    def parse(self, data):
        hunger, thirst, exhaustion, happiness = data['feelings']
        result = dict(
            name='feelings',
            user_id=data['user_id'],
            timestamp=data['timestamp'],
            feelings=dict(
                hunger=hunger,
                thirst=thirst,
                exhaustion=exhaustion,
                happiness=happiness
            )
        )
        return result
