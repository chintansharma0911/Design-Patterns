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



class Chain:
    def __init__(self):
        self.middlewares = []

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def handle_request(self, request):
        for middleware in self.middlewares:
            request = middleware.handle_request(request)
            if request is None:
                print("Request processing stopped.")
                break

if __name__ == "__main__":
    # Create middleware instances.
    auth_middleware = AuthenticationMiddleware()
    logging_middleware = LoggingMiddleware()
    data_validation_middleware = DataValidationMiddleware()

    # Create the chain and add middleware.
    chain = Chain()
    chain.add_middleware(auth_middleware)
    chain.add_middleware(logging_middleware)
    chain.add_middleware(data_validation_middleware)

    # Simulate an HTTP request.
    http_request = {"user": "username", "data": "valid_data"}
    chain.handle_request(http_request)