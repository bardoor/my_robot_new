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


def end() -> None:
    _sender.close()
    