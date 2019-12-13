import datetime
import json
import os
import numpy

from .protocol import Snapshot
from matplotlib.pyplot import imshow
import matplotlib.cm
from PIL import Image


class Parser:
    parsers = {}

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def load_parsers(self):
        pass  # TODO dynamically load all modules

    def get_path(self, user_id, timestamp):
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=timestamp)
        formatted = date.strftime("%Y-%m-%d_%H-%M-%S-%f")
        return f'{self.data_dir}/{user_id}/{formatted}'

    @staticmethod
    def parser(name):

        def decorator(cls):
            Parser.parsers[name] = cls
            return cls

        return decorator


def create_path_dirs(path):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


@Parser.parser('pose')
class PoseParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        x, y, z = snapshot.translation
        path = f'{self.get_path(user_id, snapshot.timestamp)}/translation.json'
        create_path_dirs(path)
        with open(path, 'w') as f:
            f.write(json.dumps({'x': x, 'y': y, 'z': z}))
        x, y, z, w = snapshot.rotation
        path = f'{self.get_path(user_id, snapshot.timestamp)}/rotation.json'
        with open(path, 'w') as f:
            f.write(json.dumps({'x': x, 'y': y, 'z': z, 'w': w}))


@Parser.parser('color_image')
class ColorImageParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        width, height, data = snapshot.image
        path = f'{self.get_path(user_id, snapshot.timestamp)}/color_image.jpg'
        create_path_dirs(path)

        image = Image.frombytes('RGB', (width, height), data)
        image.save(path)


@Parser.parser('depth_image')
class DepthImageParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        width, height, data = snapshot.image_depth
        path = f'{self.get_path(user_id, snapshot.timestamp)}/depth_image.jpg'
        imshow(numpy.reshape(data, (width, height)), cmap=matplotlib.cm.RdYlGn)
        matplotlib.pyplot.savefig(path)


@Parser.parser('feelings')
class FeelingsParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        hunger, thirst, exhaustion, happiness = snapshot.feelings
        path = f'{self.get_path(user_id, snapshot.timestamp)}/feelings.json'
        create_path_dirs(path)
        with open(path, 'w') as f:
            f.write(json.dumps(dict(
                hunger=hunger,
                thirst=thirst,
                exhaustion=exhaustion,
                happiness=happiness
            )))


@Parser.parser('location')
class Location(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        pass  # TBD
