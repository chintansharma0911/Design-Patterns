from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# =====================================================
# 1. DECORATOR PATTERN (Notification Content)
# =====================================================

class INotification(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class SimpleNotification(INotification):
    def __init__(self, text: str):
        self.text = text

    def get_content(self) -> str:
        return self.text


class INotificationDecorator(INotification):
    def __init__(self, notification: INotification):
        self.notification = notification


class TimestampDecorator(INotificationDecorator):
    def get_content(self) -> str:
        return f"{datetime.now()} | {self.notification.get_content()}"


class SignatureDecorator(INotificationDecorator):
    def get_content(self) -> str:
        return f"{self.notification.get_content()}\n-- System"


# =====================================================
# 2. OBSERVER PATTERN
# =====================================================

class IObserver(ABC):
    @abstractmethod
    def update(self, notification :INotification):
        pass


class IObservable(ABC):
    @abstractmethod
    def add(self, observer: IObserver):
        pass

    @abstractmethod
    def remove(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self):
        pass


class NotificationObservable(IObservable):

    def __init__(self):
        self.observers: List[IObserver] = []
        self.notification: INotification | None = None

    def set_notification(self, notification: INotification):
        self.notification = notification
        self.notify()

    def get_notification(self) -> INotification:
        return self.notification

    def add(self, observer: IObserver):
        self.observers.append(observer)

    def remove(self, observer: IObserver):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.notification)


# =====================================================
# 3. STRATEGY PATTERN (Sending Channels)
# =====================================================

class INotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, content: str):
        pass


class EmailStrategy(INotificationStrategy):
    def send_notification(self, content: str):
        print(f"📧 EMAIL SENT: {content}")


class SMSStrategy(INotificationStrategy):
    def send_notification(self, content: str):
        print(f"📱 SMS SENT: {content}")


class PopupStrategy(INotificationStrategy):
    def send_notification(self, content: str):
        print(f"🔔 POPUP SHOWN: {content}")


# =====================================================
# 4. OBSERVERS
# =====================================================

class Logger(IObserver):

    def update(self, notification):
        print(f"📝 LOGGED: {notification.get_content()}")


class NotificationEngine(IObserver):

    def __init__(self,
                 strategies: List[INotificationStrategy]):
        self.strategies = strategies

    def update(self, notification):
        content = notification.get_content()

        for strategy in self.strategies:
            strategy.send_notification(content)


# =====================================================
# 5. FACADE / ORCHESTRATOR (Notification Service)
# =====================================================

class NotificationService:

    def __init__(self):
        self.observable = NotificationObservable()

        self.logger = Logger()

        self.engine = NotificationEngine(
            strategies=[
                EmailStrategy(),
                SMSStrategy(),
                PopupStrategy()
            ]
        )

        self.observable.add(self.logger)
        self.observable.add(self.engine)

    def send_notification(self, notification: INotification):
        self.observable.set_notification(notification)


# =====================================================
# 6. CLIENT / MAIN EXECUTION
# =====================================================

if __name__ == "__main__":

    service = NotificationService()

    # Step 1: Create base notification
    notification = SimpleNotification("Your order has been confirmed!")

    # Step 2: Add decorators dynamically
    notification = TimestampDecorator(notification)
    notification = SignatureDecorator(notification)

    # Step 3: Send notification
    service.send_notification(notification)
