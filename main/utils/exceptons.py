# DB Exceptions
class DBException(Exception):
    ...


class DBNotFound(DBException):
    ...


# Custom validation exceptions
class AppValidationError(ValueError):
    ...


class IdValidationError(AppValidationError):
    ...
