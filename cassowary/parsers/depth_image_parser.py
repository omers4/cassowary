import os

from .parsers import parser
from ..utils.binary_utils import binary_from_stream
from .base_parser import BaseParser
from matplotlib.pyplot import imshow
import matplotlib.cm
import numpy


@parser('depth_image')
class DepthImageParser(BaseParser):
    def parse(self, data):
        """
        :return: This parser receives the path to the raw depth
        image data and parses it to a depth image,
        then saving it in a different location.
        """
        width, height, from_path, to_path = data['depth_image']
        with open(from_path, 'rb') as raw_image:
            img_data = binary_from_stream(raw_image, f'{width * height}f')
        os.remove(from_path)

        imshow(numpy.reshape(img_data, (width, height)), cmap=matplotlib.cm.RdYlGn)
        matplotlib.pyplot.savefig(to_path)

        result = {'name': 'depth_image',
                  'user_id': data['user_id'],
                  'timestamp': data['timestamp'],
                  'depth_image': {'path': to_path}}
        return result
