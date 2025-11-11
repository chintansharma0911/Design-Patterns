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



if __name__ == "__main__":
    # Create files
    file1 = File("resume.pdf", 120)
    file2 = File("photo.jpg", 450)
    file3 = File("song.mp3", 5000)
    file4 = File("notes.txt", 30)

    # Create directories
    documents = Directory("Documents")
    pictures = Directory("Pictures")
    music = Directory("Music")
    root = Directory("Root")

    # Build tree
    documents.add(file1)
    documents.add(file4)

    pictures.add(file2)
    music.add(file3)

    root.add(documents)
    root.add(pictures)
    root.add(music)
    root.add(File('Chintan', 100))

    # Show structure
    print("📂 File System Structure:")
    root.showDetails()

    # Show total size
    print("\n📊 Total Size:", root.getSize(), "KB")