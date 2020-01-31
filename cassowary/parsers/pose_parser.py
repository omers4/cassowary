from .parsers import parser
from .base_parser import BaseParser


@parser('pose')
class PoseParser(BaseParser):
    def parse(self, data):
        result = {'id': data['user_id'],
                  'timestamp': data['timestamp'],
                  'translation': data['translation'],
                  'rotation': data['rotation']}
        return result
