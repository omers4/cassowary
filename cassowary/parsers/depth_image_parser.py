from .parsers import parser
from .base_parser import BaseParser
from matplotlib.pyplot import imshow
import matplotlib.cm
import numpy


@parser('depth_image')
class DepthImageParser(BaseParser):
    def parse(self, data):
        width, height, from_path, to_path = data['depth_image']
        with open(from_path, 'rb') as raw_image:
            img_data = raw_image.read()
            imshow(numpy.reshape(img_data, (width, height)), cmap=matplotlib.cm.RdYlGn)
            matplotlib.pyplot.savefig(to_path)
            result = {'id': data['user_id'],
                      'timestamp': data['timestamp'],
                      'depth_image_path': to_path}
            return result
