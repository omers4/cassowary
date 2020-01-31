import datetime
import os


def create_path_dirs(path):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_path(data_dir, user_id, timestamp):
    date = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=timestamp)
    formatted = date.strftime("%Y-%m-%d_%H-%M-%S-%f")
    return f'{data_dir}/{user_id}/{formatted}'
