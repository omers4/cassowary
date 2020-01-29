class SnapshotFile:
    def __init__(self, sample_path, file_reader):
        self.file_reader = file_reader(sample_path)
        self.thoughts = SnapshotFile.Iterator(self.file_reader)

    def __enter__(self):
        self.user = self.file_reader.read_user()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_reader.file.close()

    def __repr__(self):
        return f'SnapshotFile(user={self.user})'

    class Iterator:
        def __init__(self, file_reader):
            self.file_reader = file_reader

        def __iter__(self):
            return self

        def __next__(self):
            return self.file_reader.next_snapshot()
