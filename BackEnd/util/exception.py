class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

class ValidationError(CustomError):
    pass

class AlreadyExistError(CustomError):
    pass

class InvalidRequest(CustomError):
    pass

class ProcessingFailureError(CustomError):
    pass

