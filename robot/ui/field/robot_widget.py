from typing import override

import pygame as pg

from robot.model.field import Robot, Cell
from robot.model.event.listeners import RobotListener
from robot.ui.field.widget import Widget


class RobotWidget(Widget, RobotListener):
    ROBOT_SIZE = 20
    ROBOT_COLOR = pg.color.THECOLORS['red']

    def __init__(self, robot: Robot) -> None:
        self._robot = robot
        self._surface = self._make_robot_surface()

    def _make_robot_surface(self) -> pg.Surface:
        surface = pg.Surface((RobotWidget.ROBOT_SIZE, RobotWidget.ROBOT_SIZE))
        surface.fill(RobotWidget.ROBOT_COLOR)
        return surface

    @override
    def render(self) -> pg.Surface:
        return self._surface

    @override
    def on_robot_moved(self, from_cell: Cell, to_cell: Cell) -> None:
        pass

    @override
    def on_robot_not_moved(self) -> None:
        pass

    @override
    def on_robot_painted_cell(self) -> None:
        pass
