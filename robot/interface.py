from robot.model.direction import Direction
from robot.ipc.sender import Sender as _Sender


NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
WEST = Direction.WEST
EAST = Direction.EAST


_sender = _Sender()
_sender.connect()


def step(direction: Direction) -> None:
    command = {"command": "step", "direction": str(direction)}
    _sender.send(command)


def paint() -> None:
    command = {"command": "paint"}
    _sender.send(command)


def is_wall(direction: Direction) -> bool:
    command = {"command": "is_wall", "direction": str(direction)}
    response = _sender.send(command, need_answer=True)
    return response["result"]


def end() -> None:
    command = {"command": "quit"}
    _sender.send(command)


def load_field(file_name: str) -> None:
    command = {"command": "load", "field": file_name}
    _sender.send(command)

