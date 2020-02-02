from .parsers import parser
from .base_parser import BaseParser


@parser('pose')
class PoseParser(BaseParser):
    def parse(self, data):
        result = {
            'name': 'pose',
            'user_id': data['user_id'],
            'timestamp': data['timestamp'],
            'pose': {
                'translation': data['translation'],
                'rotation': data['rotation']}
            }
        return result
