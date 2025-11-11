from abc import ABC, abstractmethod

# ------------------- Receiver Classes -------------------
class LightBulb:
    def on(self):
        print("💡 Light is ON")

    def off(self):
        print("💡 Light is OFF")


class AirConditioner:
    def on(self):
        print("❄️ AC is ON")

    def off(self):
        print("❄️ AC is OFF")


# ------------------- Command Interface -------------------
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ------------------- Concrete Commands -------------------
class LightOnCommand(Command):
    def __init__(self, light: LightBulb):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: LightBulb):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()


class ACOnCommand(Command):
    def __init__(self, ac: AirConditioner):
        self.ac = ac

    def execute(self):
        self.ac.on()

    def undo(self):
        self.ac.off()


class ACOffCommand(Command):
    def __init__(self, ac: AirConditioner):
        self.ac = ac

    def execute(self):
        self.ac.off()

    def undo(self):
        self.ac.on()


# ------------------- Invoker with Undo/Redo -------------------
class RemoteControl:
    def __init__(self):
        self.history = []   # stack for undo
        self.redo_stack = []  # stack for redo

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()  # once a new command is executed, redo history clears

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)
        else:
            print("Nothing to undo")

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)
        else:
            print("Nothing to redo")


if __name__ == "__main__":
    # Receivers
    light = LightBulb()
    ac = AirConditioner()

    # Commands
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)
    ac_on = ACOnCommand(ac)
    ac_off = ACOffCommand(ac)

    # Invoker
    remote = RemoteControl()

    # Use case
    remote.execute_command(light_on)   # 💡 Light is ON
    remote.execute_command(ac_on)      # ❄️ AC is ON
    remote.undo()                      # ❄️ AC is OFF
    remote.undo()                      # 💡 Light is OFF
    remote.redo()                      # 💡 Light is ON
    remote.execute_command(ac_off)     # ❄️ AC is OFF
    remote.redo()                      # Nothing to redo
