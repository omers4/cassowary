

def upload_sample(host: str, port: int, path: str):  #, reader=BinaryReader):
    try:
        print(f'Start uploading the snapshot in {path} to {host}:{port}')
        # with Reader(path, reader) as reader:
        #     upload_snapshot(address, reader)
        print('Done uploading the snapshot')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
