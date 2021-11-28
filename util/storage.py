import abc


class StorageClient(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def open(self, output):
        return

    @abc.abstractclassmethod
    def save(self, data):
        return

    @abc.abstractclassmethod
    def close(self):
        return
