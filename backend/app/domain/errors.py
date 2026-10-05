class DomainError(Exception):
    def __init__(self, code: str, message: str, details: dict | None = None, status: int = 400):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status = status
        super().__init__(message)

def not_found(message="Resource not found"):
    return DomainError("RESOURCE_NOT_FOUND", message, status=404)

def forbidden(message="Forbidden"):
    return DomainError("FORBIDDEN", message, status=403)

def invalid(message, details=None):
    return DomainError("INVALID_REQUEST", message, details=details, status=422)

def conflict(code, message, details=None):
    return DomainError(code, message, details=details, status=409)
