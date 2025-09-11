from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def saveFile(self):
        pass


class AdvanceFileStorage(FileStorage):
    def __init__(self, implementation):
        self._implementation = implementation

    def saveFile(self):
        self._implementation.save()


class StorageImplementation(ABC):
    @abstractmethod
    def save(self):
        pass


class LocalStorage(StorageImplementation):
    def save(self):
        print('Saved to local')


class CloudStorage(StorageImplementation):
    def save(self):
        print('Saved to cloud')


class Networktorage(StorageImplementation):
    def save(self):
        print('Saved to network')
