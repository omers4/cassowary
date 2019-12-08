import struct

from .utils.binary_utils import binary_from_file
from .utils.protocol import Snapshot


class Reader:
    def __init__(self, sample_path):
        self.sample_path = sample_path
        self.thoughts = Reader.Iterator(self)

    def __enter__(self):
        self.file = open(self.sample_path, 'rb')
        self.user_id, user_name_length = binary_from_file(self.file, 'QI')
        self.user_name = binary_from_file(self.file, f'{user_name_length}s')[0].decode('ASCII')
        self.birth, self.gender = binary_from_file(self.file, 'Ic')
        self.gender = self.gender.decode('ASCII')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def __repr__(self):
        return f'Reader(user_id={self.user_id}, user_name={self.user_name},' \
               f'birth={self.birth}, gender={self.gender})'

    class Iterator:
        def __init__(self, reader):
            self.cursor = reader

        def __iter__(self):
            return self

        def __next__(self):
            timestamp, translation_x, translation_y, translation_z, \
                rotation_x, rotation_y, rotation_z, rotation_w, \
                height, width = binary_from_file(self.cursor.file, 'QdddddddII')

            if timestamp is None:
                raise StopIteration()

            pixels = binary_from_file(self.cursor.file, f'{3*height*width}b')
            depth_height, depth_width = binary_from_file(self.cursor.file, 'II')
            depth_pixels = binary_from_file(self.cursor.file, f'{depth_height*depth_width}f')

            hunger, thirst, exhaustion, happiness = binary_from_file(self.cursor.file, 'ffff')

            snapshot = Snapshot(timestamp, (translation_x, translation_y, translation_z),
                                (rotation_x, rotation_y, rotation_z, rotation_w),
                                (width, height, pixels),
                                (depth_width, depth_height, depth_pixels),
                                hunger, thirst, exhaustion, happiness)

            return snapshot
