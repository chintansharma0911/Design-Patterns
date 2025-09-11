from abc import ABC, abstractmethod


class FileSystemComponent(ABC):

    @abstractmethod
    def showDetails(self, indent=0):
        pass

    @abstractmethod
    def getSize(self):
        pass


class File(FileSystemComponent):

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def showDetails(self, indent=0):
        print(" " * indent + f"- File: {self.name} ({self.size} KB)")

    def getSize(self):
        return self.size


class Directory(FileSystemComponent):

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, data):
        self.children.append(data)

    def showDetails(self, indent=0):
        print(" " * indent + f"[Dir] {self.name}/")
        for child in self.children:
            child.showDetails(indent +4)

    def getSize(self):
        total = 0
        for child in self.children:
            total += child.getSize()
        return total
