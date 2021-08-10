from typing import List, Optional

from .errors import DuplicateCommand, NameHasSpaces


class Command:
    """Represents a cli command."""

    def __init__(self, **attrs) -> None:
        self._func = attrs["_func"]
        self.name = attrs["name"] or self._func.__name__
        self.description: str = (
            attrs["description"] or self._func.__doc__ or "No description given."
        )


class CommandGroup(Command):
    """Represents a group of cli commands."""

    def __init__(self, **attrs) -> None:
        super().__init__(**attrs)
        self.children: List[Command] = []

    def command(self, name: Optional[str] = None, description: Optional[str] = None):
        def decorator(func):
            command = Command(name=name, description=description, _func=func)
            if command in self.children:
                raise DuplicateCommand(
                    f"A subcommand for this group with the name {command.name} already exists."
                )
            elif command.name.count(" ") > 0:
                raise NameHasSpaces("Command names can't have spaces.")
            self.children.append(command)
            return command

        return decorator

    def get_subcommand(self, name: str):
        for command in self.children:
            if command.name == name:
                return command
