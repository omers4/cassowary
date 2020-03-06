import gzip
from ..utils.binary_utils import read_message_by_length
from ..utils.cortex_pb2 import User as ProtobuffUser, \
    Snapshot as ProtobuffSnapshot
from ..utils.protocol import Snapshot, User
from .base_reader import BaseReader


class ProtobuffReader(BaseReader):
    def __init__(self, sample_path):
        self.file = gzip.open(sample_path, 'rb')

    def read_user(self):
        user_raw = read_message_by_length(self.file)
        pb_user = ProtobuffUser()
        pb_user.ParseFromString(user_raw)

        user = User(pb_user.user_id, pb_user.username, pb_user.birthday,
                    'f' if pb_user.gender == 1 else 'm')
        return user

    def next_snapshot(self):
        snapshot_raw = read_message_by_length(self.file)

        if snapshot_raw is None:
            raise StopIteration()

        pb_snapshot = ProtobuffSnapshot()
        pb_snapshot.ParseFromString(snapshot_raw)

        snapshot = Snapshot(pb_snapshot.datetime,
                            (pb_snapshot.pose.translation.x,
                             pb_snapshot.pose.translation.y,
                             pb_snapshot.pose.translation.z),
                            (pb_snapshot.pose.rotation.x,
                             pb_snapshot.pose.rotation.y,
                             pb_snapshot.pose.rotation.z,
                             pb_snapshot.pose.rotation.w),
                            (pb_snapshot.color_image.width,
                             pb_snapshot.color_image.height,
                             pb_snapshot.color_image.data),
                            (pb_snapshot.depth_image.width,
                             pb_snapshot.depth_image.height,
                             pb_snapshot.depth_image.data),
                            pb_snapshot.feelings.hunger,
                            pb_snapshot.feelings.thirst,
                            pb_snapshot.feelings.exhaustion,
                            pb_snapshot.feelings.happiness)
        return snapshot
