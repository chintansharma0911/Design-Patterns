class Request:
    def __init__(self, data):
        self.data = data
        self.valid = True


class RequestHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, request):
        if self.successor:
            self.successor.handle_request(request)


class AuthenticationHandler(RequestHandler):
    def handle_request(self, request):
        if "token" not in request.data:
            request.valid = False
            print("Authentication failed")
        super().handle_request(request)


class DataValidationHandler(RequestHandler):
    def handle_request(self, request):
        if not request.valid:
            return
        if "data" not in request.data:
            request.valid = False
            print("Data validation failed")
        super().handle_request(request)


class LoggingHandler(RequestHandler):
    def handle_request(self, request):
        if not request.valid:
            return
        print("Logging request")
        super().handle_request(request)
