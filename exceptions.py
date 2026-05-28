from http import HTTPStatus


class BusinessError(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code


class NotFoundError(BusinessError):
    def __init__(self, message: str) -> None:
        super().__init__(message, HTTPStatus.NOT_FOUND)


class ConflictError(BusinessError):
    def __init__(self, message: str) -> None:
        super().__init__(message, HTTPStatus.CONFLICT)


class UnauthorizedError(BusinessError):
    def __init__(self, message: str) -> None:
        super().__init__(message, HTTPStatus.UNAUTHORIZED)


class ForbiddenError(BusinessError):
    def __init__(self, message: str) -> None:
        super().__init__(message, HTTPStatus.FORBIDDEN)