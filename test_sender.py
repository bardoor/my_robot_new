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


step(Direction.EAST)
step(Direction.EAST)
paint()

sender.close()