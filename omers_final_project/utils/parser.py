import json
import os

from .protocol import Snapshot
from PIL import Image


class Parser:
    parsers = {}

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_path(self, user_id, timestamp):
        return f'{self.data_dir}/{user_id}/{timestamp}'

    @staticmethod
    def parser(name):

        def decorator(cls):
            Parser.parsers[name] = cls
            return cls

        return decorator


def create_path_dirs(path):
    dir_path = os.path.dirname(path)
    print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# @Parser.parser('translation')
class TranslationParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        x, y, z = snapshot.translation
        path = f'{self.get_path(user_id, snapshot.timestamp)}/translation.json'
        create_path_dirs(path)
        with open(path, 'w') as f:
            f.write(json.dumps({'x': x, 'y': y, 'z': z}))


@Parser.parser('color_image')
class ColorImageParser(Parser):
    def parse(self, user_id: int, snapshot: Snapshot):
        width, height, data = snapshot.image
        path = f'{self.get_path(user_id, snapshot.timestamp)}/color_image.jpg'
        create_path_dirs(path)

        image = Image.new('RGB', (width, height))

        for i, pixel in enumerate(data):
            data = (pixel[0], pixel[1], pixel[2])

        print(data[0])

        image.putdata(data)
        image.save(path)
        print(f'saved image to {path}')
