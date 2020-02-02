from .parsers import parser
from .base_parser import BaseParser


@parser('personal_details')
class PersonalDetailsParser(BaseParser):
    def parse(self, data):
        result = {
            'name': 'personal_details',
            'user_id': data['user_id'],
            'personal_details': {
                'user_id': data['user_id'],
                'user_name': data['user_name'],
                'birth': data['birth'],
                'gender': data['gender']
            }
        }
        return result
