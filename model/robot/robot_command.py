from ..direction import Direction
from abc import ABC


class RobotCommand(ABC):
    def __init__(self, robot=None):
        self._robot = robot

    def execute(self):
        pass

    def set_robot(self, robot):
        self._robot = robot


class Step(RobotCommand):
    def __init__(self, direction: Direction, robot=None):
        super().__init__(robot)
        self.__direction = direction

    def execute(self):
        if self._robot is None:
            raise Exception("Робот не задан")

        self._robot.step(self.__direction)


class Paint(RobotCommand):
    def __init__(self, robot=None):
        super().__init__(robot)

    def execute(self) -> bool:
        if self._robot is None:
            raise Exception("Робот не задан")

        self._robot.paint()