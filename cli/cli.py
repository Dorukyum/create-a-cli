from sys import argv
from typing import List, Optional, Union

from .command import Command, CommandGroup
from .errors import CommandNotFound, DuplicateCommand, NameHasSpaces


class Interface:
    def __init__(self, name: str):
        self.name = name
        self.commands: List[Union[Command, CommandGroup]] = []

        def default_help(command=None, subcommand=None):
            if command:
                command = self.get_command(command)
                if command:
                    if type(command) == CommandGroup:
                        if subcommand:
                            _subcommand = command.get_subcommand(subcommand)
                            if _subcommand:
                                print(_subcommand.description)
                            else:
                                raise CommandNotFound(
                                    f"Subcommand {subcommand} of command group {command.name} wasn't found."
                                )
                        else:
                            print(
                                f"Subcommands: {', '.join(cmd.name for cmd in command.children)}"
                            )
                    else:
                        print(command.description)
                else:
                    print(f"Command {argv[1]} not found.")
            else:
                print(f"Command list: {', '.join(cmd.name for cmd in self.commands)}")

        self.help_command = Command(
            name="help", description="Get help about the cli.", _func=default_help
        )

    def command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        def decorator(func):
            command = Command(
                name=name,
                description=description,
                _func=func,
            )
            if command.name == "help":
                self.help_command = func
            elif command in self.commands:
                raise DuplicateCommand(
                    f"A command with the name {command.name} already exists."
                )
            elif command.name.count(" ") > 0:
                raise NameHasSpaces("Command names can't have spaces.")
            self.commands.append(command)
            return command

        return decorator

    def group(self, name: Optional[str] = None, description: Optional[str] = None):
        def decorator(func):
            command = CommandGroup(name=name, description=description, _func=func)
            if command.name == "help":
                self.help_command = func
            elif command in self.commands:
                raise DuplicateCommand(
                    f"A command with the name {command.name} already exists."
                )
            elif command.name.count(" ") > 0:
                raise NameHasSpaces("Command group names can't have spaces.")
            self.commands.append(command)
            return command

        return decorator

    def get_command(self, name: str):
        if name == "help":
            return self.help_command

        for command in self.commands:
            if command.name == name:
                return command

    def remove_command(self, command: Union[str, Command]):
        if type(command) == str:
            command = self.get_command(command)
        self.commands.remove(command)

    def run(self, interactive: bool = True):
        if interactive:
            args = input(">>> ").split()
            while len(args) > 0 and args[0] not in ("exit", "quit"):
                command = self.get_command(args[0])
                if not command:
                    raise CommandNotFound(f"Command {args[0]} wasn't found.")

                if type(command) == Command or len(args) == 1:
                    command._func(*args[1:])
                else:
                    for subcommand in command.children:
                        if subcommand.name == args[1]:
                            subcommand._func(*args[2:])
                            break
                    else:
                        raise CommandNotFound(
                            f"Subcommand {args[1]} of command group {args[0]} wasn't found."
                        )
                args = input(">>> ").split()
        elif len(argv) == 1:
            self.help_command._func()
        else:
            command = self.get_command(argv[1])
            if not command:
                raise CommandNotFound(f"Command {argv[1]} wasn't found.")

            if type(command) == Command or len(argv) == 2:
                command._func(*argv[2:])
            else:
                for subcommand in command.children:
                    if subcommand.name == argv[2]:
                        subcommand._func(*argv[3:])
                        break
                else:
                    raise CommandNotFound(
                        f"Subcommand {argv[2]} of command group {argv[1]} wasn't found."
                    )
