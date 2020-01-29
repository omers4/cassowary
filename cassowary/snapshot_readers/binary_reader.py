from ..utils.binary_utils import binary_from_stream
from ..utils.protocol import User, Snapshot
from .base_reader import BaseReader


class BinaryReader(BaseReader):
    def __init__(self, sample_path):
        self.file = open(sample_path, 'rb')

    def read_user(self):
        user_id, user_name_length = binary_from_stream(self.file, 'QI')
        user_name = binary_from_stream(self.file, f'{user_name_length}s')[0].decode('ASCII')
        birth, gender = binary_from_stream(self.file, 'Ic')
        gender = gender.decode('ASCII')
        return User(user_id, user_name, birth, gender)

    def next_snapshot(self):
        timestamp, translation_x, translation_y, translation_z, \
        rotation_x, rotation_y, rotation_z, rotation_w, \
        height, width = binary_from_stream(self.file, 'QdddddddII')

        if timestamp is None:
            raise StopIteration()

        pixels = self.file.read(3 * height * width)
        depth_height, depth_width = binary_from_stream(self.file, 'II')
        depth_pixels = binary_from_stream(self.file, f'{depth_height * depth_width}f')

        hunger, thirst, exhaustion, happiness = binary_from_stream(self.file, 'ffff')

        snapshot = Snapshot(timestamp, (translation_x, translation_y, translation_z),
                            (rotation_x, rotation_y, rotation_z, rotation_w),
                            (width, height, pixels),
                            (depth_width, depth_height, depth_pixels),
                            hunger, thirst, exhaustion, happiness)

        return snapshot
