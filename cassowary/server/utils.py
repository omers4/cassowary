import datetime
import os


def create_path_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_path(data_dir, user_id, timestamp, name):
    date = datetime.datetime(1970, 1, 1) + \
           datetime.timedelta(milliseconds=timestamp)
    formatted = date.strftime("%Y-%m-%d_%H-%M-%S-%f")
    return f'{data_dir}/{user_id}_{formatted}_{name}'
