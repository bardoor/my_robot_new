from robot.model.direction import Direction
from robot.model.robot.robot import StepResult
from robot.ipc.proxy import Proxy as Proxy


NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
WEST = Direction.WEST
EAST = Direction.EAST


class RobotHitWallError(RuntimeError):
    pass


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
    step_result = _proxy.step(direction)
    if step_result == StepResult.HIT_WALL:
        raise RobotHitWallError("Робот врезался в стену")


@_connect
def paint() -> None:
    _proxy.paint()


@_connect
def is_wall(direction: Direction) -> bool:
    return _proxy.is_wall(direction)
