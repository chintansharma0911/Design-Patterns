from abc import ABC, abstractmethod


class Middleware(ABC):

    @abstractmethod
    def handle_request(self, request):
        return request


class AuthenticationMiddleware(Middleware):

    def handle_request(self, request):
        if self.authenticate(request):
            print("Authentication middleware: Authenticated successfully")
            return super().handle_request(request)
        else:
            print("Authentication middleware: Authentication failed")
            return None

    def authenticate(self, request):
        return True


class LoggingMiddleware(Middleware):

    def handle_request(self, request):
        print("Logging middleware: Logging request")
        return super().handle_request(request)


class DataValidationMiddleware(Middleware):

    def handle_request(self, request):
        if self.validate_data(request):
            print("Data Validation middleware: Data is valid")
            return super().handle_request(request)
        else:
            print("Data Validation middleware: Invalid data")
            return None

    def validate_data(self, request):
        return True