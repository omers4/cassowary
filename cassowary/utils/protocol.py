import struct
from .binary_utils import binary_from_stream


class User:
    def __init__(self, user_id, user_name, birth, gender):
        self.user_id = user_id
        self.user_name = user_name
        self.birth = birth
        self.gender = gender

    def __repr__(self):
        return f'User(user_id={self.user_id}, ' \
               f'user_name="{self.user_name}", ' \
               f'birth={self.birth}, ' \
               f'gender={self.gender})'


class Hello:
    def __init__(self, user: User):
        self.user = user

    def __repr__(self):
        return f'Hello(user_id={self.user.user_id}, ' \
               f'user_name="{self.user.user_name}", ' \
               f'birth={self.user.birth}, ' \
               f'gender={self.user.gender})'

    def serialize(self):
        return struct.pack(f'<QI{len(self.user.user_name)}sIc',
                           self.user.user_id,
                           len(self.user.user_name),
                           bytes(self.user.user_name, 'ASCII'),
                           self.user.birth,
                           bytes(self.user.gender, 'ASCII'))

    @staticmethod
    def deserialize(stream):
        user_id, user_name_length = binary_from_stream(stream, '<QI')
        user_name = binary_from_stream(stream, f'{user_name_length}s')[
            0].decode('ASCII')
        birth, gender = binary_from_stream(stream, '<Ic')
        return Hello(User(user_id, user_name, birth, gender.decode('ASCII')))


class Config:
    def __init__(self, fields):
        self.fields = fields

    def __repr__(self):
        return f'Config(fields={self.fields})'

    def serialize(self):
        params = [len(self.fields)]
        struct_format = '<I'
        for field in self.fields:
            struct_format += f'I{len(field)}s'
            params.append(len(field))
            params.append(bytes(field, 'ASCII'))
        return struct.pack(struct_format, *params)

    @staticmethod
    def deserialize(stream):
        list_length = binary_from_stream(stream, '<I')[0]
        fields = []
        for i in range(0, list_length):
            field_length = binary_from_stream(stream, '<I')[0]
            field = binary_from_stream(stream, f'{field_length}s')[0]
            fields.append(field.decode('ASCII'))
        return Config(fields)


class Snapshot:
    def __init__(self, timestamp, translation, rotation, image: tuple,
                 image_depth, hunger, thirst, exhaustion, happiness):

        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.image = image
        self.image_depth = image_depth
        self.feelings = hunger, thirst, exhaustion, happiness

    def __repr__(self):
        return f'Snapshot(timestamp={self.timestamp}, ' \
               f'translation={self.translation}, ' \
               f'rotation={self.rotation}, ' \
               f'feelings={self.feelings}' \
               f')'

    def serialize(self, fields):
        if 'pose' in fields:
            translation = self.translation
            rotation = self.rotation
        else:
            translation = (0, 0, 0)
            rotation = (0, 0, 0, 0)
        feelings = self.feelings if 'feelings' in fields else (0, 0, 0, 0)
        w, h, data = self.image if 'color_image' in fields else (0, 0, b'')
        d_w, d_h, d_data = self.image_depth if 'depth_image' in fields else (
            0, 0, [])

        params = [self.timestamp, *translation, *rotation, h, w]
        if data:
            params.append(data)
        params.extend([d_w, d_h])
        params.extend(d_data)
        return struct.pack(f'<QdddddddII{len(data)}sII{len(d_data)}fffff',
                           *params, *feelings)

    @staticmethod
    def deserialize(stream, fields):
        timestamp, translation_x, translation_y, translation_z, \
            rotation_x, rotation_y, rotation_z, rotation_w, \
            height, width = binary_from_stream(stream, 'QdddddddII')

        pixels = None
        if 'color_image' in fields:
            pixels = binary_from_stream(stream, f'{3 * height * width}s')[0]
        depth_height, depth_width = binary_from_stream(stream, 'II')

        depth_pixels = None
        if 'depth_image' in fields:
            depth_pixels = binary_from_stream(stream,
                                              f'{depth_height * depth_width}f')

        hunger, thirst, exhaustion, happiness = binary_from_stream(stream,
                                                                   'ffff')

        return Snapshot(timestamp,
                        (translation_x, translation_y, translation_z),
                        (rotation_x, rotation_y, rotation_z, rotation_w),
                        (width, height, pixels),
                        (depth_width, depth_height, depth_pixels),
                        hunger, thirst, exhaustion, happiness)
