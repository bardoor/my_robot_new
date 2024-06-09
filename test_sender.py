from robot.ipc.proxy import Proxy
from robot.model.direction import Direction


sender = Proxy()
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


paint()

if is_wall(Direction.EAST):
    print("На востоке стена")
else:
    print("Стены на востоке нет")

if not is_wall(Direction.SOUTH):
    step(Direction.SOUTH)
    print("Я сдвинулся")