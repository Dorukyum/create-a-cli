class DuplicateCommand(BaseException):
    """Raised when multiple commands have the same name."""


class NameHasSpaces(BaseException):
    """Raised when a command name has spaces."""


class CommandNotFound(BaseException):
    """Raised when no command with the given name exists."""
