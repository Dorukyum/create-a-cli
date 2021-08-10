from cli import Interface

cli = Interface("ExampleCLI")


@cli.group()
def math():
    """Math commands"""


@math.command()
def add(*numbers):
    """Prints the sum of the supplied numbers."""
    print(sum(map(int, numbers)))


cli.run()
