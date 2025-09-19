from abc import ABC, abstractmethod
from enum import Enum
import time
import json


# -----------------------------
# Log Levels
# -----------------------------
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5


# -----------------------------
# Log Message
# -----------------------------
class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.level = level
        self.message = message
        self.timestamp = int(time.time() * 1000)  # milliseconds


# -----------------------------
# Log Formatter
# -----------------------------
class LogFormatter(ABC):
    @abstractmethod
    def format(self, log_message: LogMessage) -> str:
        pass


class PlainTextFormatter(LogFormatter):
    def format(self, log_message: LogMessage) -> str:
        return f"[{log_message.level.name}] {log_message.timestamp} : {log_message.message}"


class JsonFormatter(LogFormatter):
    def format(self, log_message: LogMessage) -> str:
        return json.dumps({
            "level": log_message.level.name,
            "timestamp": log_message.timestamp,
            "message": log_message.message
        })


# -----------------------------
# Log Appenders
# -----------------------------
class LogAppender(ABC):
    def __init__(self, formatter: LogFormatter):
        self.formatter = formatter

    @abstractmethod
    def append(self, log_message: LogMessage):
        pass


class ConsoleAppender(LogAppender):
    def append(self, log_message: LogMessage):
        print(self.formatter.format(log_message))


class FileAppender(LogAppender):
    def __init__(self, formatter: LogFormatter, file_name: str):
        super().__init__(formatter)
        self.file_name = file_name

    def append(self, log_message: LogMessage):
        with open(self.file_name, "a") as f:
            f.write(self.formatter.format(log_message) + "\n")


# -----------------------------
# Log Handlers (Chain of Responsibility)
# -----------------------------
class LogHandler(ABC):
    def __init__(self):
        self.next_handler = None
        self.appenders = []

    def set_next(self, handler: 'LogHandler'):
        self.next_handler = handler
        return handler

    def subscribe(self, appender: LogAppender):
        self.appenders.append(appender)

    def notify(self, log_message: LogMessage):
        for appender in self.appenders:
            appender.append(log_message)

    def handle(self, log_message: LogMessage):
        if self.can_handle(log_message.level):
            self.notify(log_message)
        if self.next_handler:
            self.next_handler.handle(log_message)

    @abstractmethod
    def can_handle(self, level: LogLevel) -> bool:
        pass


class DebugHandler(LogHandler):
    def can_handle(self, level: LogLevel) -> bool:
        return level == LogLevel.DEBUG


class WarnHandler(LogHandler):
    def can_handle(self, level: LogLevel) -> bool:
        return level == LogLevel.WARN


class ErrorHandler(LogHandler):
    def can_handle(self, level: LogLevel) -> bool:
        return level in (LogLevel.ERROR, LogLevel.FATAL)


# -----------------------------
# Logger (Singleton)
# -----------------------------
class Logger:
    _instance = None

    def __init__(self):
        if Logger._instance:
            raise Exception("Use get_instance() instead of creating Logger directly.")
        self.root_handler = None

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    def add_handler_chain(self, handler: LogHandler):
        self.root_handler = handler

    def log(self, level: LogLevel, message: str):
        if not self.root_handler:
            raise Exception("No log handler chain set!")
        log_message = LogMessage(level, message)
        self.root_handler.handle(log_message)

    # convenience methods
    def debug(self, msg): self.log(LogLevel.DEBUG, msg)
    def info(self, msg): self.log(LogLevel.INFO, msg)
    def warn(self, msg): self.log(LogLevel.WARN, msg)
    def error(self, msg): self.log(LogLevel.ERROR, msg)
    def fatal(self, msg): self.log(LogLevel.FATAL, msg)


# -----------------------------
# Client
# -----------------------------
if __name__ == "__main__":
    logger = Logger.get_instance()

    # Build Chain: Debug -> Warn -> Error
    debug_handler = DebugHandler()
    warn_handler = WarnHandler()
    error_handler = ErrorHandler()

    debug_handler.set_next(warn_handler).set_next(error_handler)

    # Subscribe appenders
    console_appender = ConsoleAppender(PlainTextFormatter())
    file_appender = FileAppender(JsonFormatter(), "logs.txt")

    debug_handler.subscribe(console_appender)
    warn_handler.subscribe(console_appender)
    error_handler.subscribe(file_appender)

    logger.add_handler_chain(debug_handler)

    # Test logging
    logger.debug("This is a debug log")
    logger.info("This is an info log")  # INFO is not handled → ignored
    logger.warn("This is a warning")
    logger.error("This is an error")
    logger.fatal("System crash!")
