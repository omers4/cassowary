import datetime
import struct

FORMAT = 'LLI'
PACK_SIZE = struct.calcsize('LLI')


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.date = datetime.datetime.fromtimestamp(timestamp)
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, ' \
               f'timestamp={self.date.__repr__()}, ' \
               f'thought="{self.thought}")'

    def __str__(self):
        return f'[{self.date}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False

        return self.user_id == other.user_id and \
            self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        print(self.user_id, self.timestamp, self.thought)
        return struct.pack(f'{FORMAT}{len(self.thought)}s',
                           int(self.user_id), int(self.timestamp),
                           len(self.thought), bytes(self.thought, 'ASCII'))

    @staticmethod
    def deserialize(data):
        user_id, timestamp, thought_size = struct.unpack(FORMAT,
                                                         data[0:PACK_SIZE])
        thought_list = struct.unpack(f'{thought_size}s', data[PACK_SIZE:])
        thought = thought_list[0].decode('ASCII')
        return Thought(user_id=user_id, timestamp=timestamp, thought=thought)
