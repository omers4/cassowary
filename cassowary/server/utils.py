import datetime
import os


def create_path_dirs(path: str):
    """
    Creates matching dir for the product, if they don't exist yet
    :param path: path of the dir we want to create
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_path(data_dir: str, user_id: str, timestamp: int, name: str):
    """
    Generates a path
    :param data_dir: the path to the dir
    :param user_id: the id of the user
    :param timestamp: the timestamp of the snapshot
    :param name: the name of the user
    :return:
    """
    date = datetime.datetime(1970, 1, 1) + \
        datetime.timedelta(milliseconds=timestamp)
    formatted = date.strftime("%Y-%m-%d_%H-%M-%S-%f")
    return f'{data_dir}/{user_id}_{formatted}_{name}'
