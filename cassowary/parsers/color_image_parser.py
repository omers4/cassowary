import os

from .parsers import parser
from .base_parser import BaseParser
from PIL import Image


@parser('color_image')
class ColorImageParser(BaseParser):
    def parse(self, data):
        """
        :return: This parser receives the path to the raw color
        image data and parses it to a color image,
        then saving it in a different location.
        """
        width, height, from_path, to_path = data['color_image']
        with open(from_path, 'rb') as raw_image:
            img_data = raw_image.read()
            image = Image.frombytes('RGB', (width, height), img_data)
            image.save(to_path)
            os.remove(from_path)
            result = {'name': 'color_image',
                      'user_id': data['user_id'],
                      'timestamp': data['timestamp'],
                      'color_image': {'path': to_path}}
            return result
