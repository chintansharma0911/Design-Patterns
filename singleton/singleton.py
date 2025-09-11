import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            with Singleton._lock:
                if Singleton._instance is None:
                    Singleton._instance = Singleton()
        return Singleton._instance

