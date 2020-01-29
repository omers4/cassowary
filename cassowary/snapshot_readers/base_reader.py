class BaseReader:
    def read_user(self):
        raise NotImplementedError()

    def next_snapshot(self):
        raise NotImplementedError()
