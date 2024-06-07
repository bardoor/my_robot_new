from robot.ipc.sender import Sender
from robot.model.direction import Direction


sender = Sender()
sender.connect()

sender.send({"command": "load", "field": "C:\\Projects\\my_robot_new\\field.json"})

def step(direction: Direction) -> None:
    command = {"command": "step", "direction": str(direction)}
    sender.send(command)


def paint() -> None:
    command = {"command": "paint"}
    sender.send(command)


def is_wall(direction: Direction) -> bool:
    command = {"command": "is_wall", "direction": str(direction)}
    response = sender.send(command, need_answer=True)
    return response["result"]


def end() -> None:
    command = {"command": "quit"}
    sender.send(command)


step(Direction.EAST)
step(Direction.EAST)
paint()

if is_wall(Direction.EAST):
    print("На востоке стена")
else:
    print("Стены на востоке нет")

if not is_wall(Direction.SOUTH):
    step(Direction.SOUTH)