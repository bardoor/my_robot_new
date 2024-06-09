from functools import partial

from .model.direction import Direction
from .ipc.proxy import Proxy as Proxy


NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
WEST = Direction.WEST
EAST = Direction.EAST


_proxy = None


def _connect(f):

    def wrapper(*args, **kwargs):
        global _proxy
        if _proxy is None:
            _proxy = Proxy()
            _proxy.connect()
        return f(*args, **kwargs)

    return wrapper


@_connect
def step(direction: Direction) -> None:
    _proxy.step(direction)


@_connect
def paint() -> None:
    _proxy.paint()


@_connect
def is_wall(direction: Direction) -> bool:
    return _proxy.is_wall(direction)


@_connect
def end() -> None:
    _proxy.end()


@_connect
def load_field(file_name: str) -> None:
    _proxy.load_field(file_name)
