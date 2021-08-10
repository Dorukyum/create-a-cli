<div align="center">
    <h1>create-a-cli</h1>
    <p style="font-size: 22px">Create command line interfaces using Python</p>
</div>


## Installation
```
[python | python3] -m [pip | pip3] install create-a-cli
```
## Usage
```python
from cli import Interface
cli = Interface("Example CLI")

@cli.command()
def hello():
    print("Hello World")

cli.run()
```
```
Command Line > python path/to/file.py
>>> hello
Hello World
```