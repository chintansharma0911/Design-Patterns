from abc import ABC, abstractmethod

# Step 1: The ChatRoom - Publisher
class ChatRoom:
    def __init__(self):
        self._participants = set()

    def join(self, participant):
        """Adds a new participant to the chat room."""
        self._participants.add(participant)

    def leave(self, participant):
        """Removes a participant from the chat room."""
        self._participants.remove(participant)

    def broadcast(self, message):
        """Sends a message to all participants in the chat room."""
        for participant in self._participants:
            participant.receive(message)

class Participant(ABC):
    @abstractmethod
    def receive(self, message):
        """Abstract method for receiving messages."""
        pass

class ChatMember(Participant):
    def __init__(self, name):
        self.name = name

    def receive(self, message):
        """Receives and displays the message."""
        print(f"{self.name} received: {message}")