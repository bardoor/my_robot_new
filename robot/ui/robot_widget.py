from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.model.event import RobotListener
from robot.ui.core import Widget


if TYPE_CHECKING:
    from robot.model.field import Cell
    from robot.model.robot import Robot


class RobotWidget(Widget, RobotListener):
    ROBOT_SIZE = 20
    ROBOT_COLOR = pg.color.THECOLORS['darkgreen']

    def __init__(self, robot: Robot) -> None:
        self._robot = robot
        self._robot.add_listener(self)

    def _make_robot_surface(self) -> pg.Surface:
        surface = pg.Surface((RobotWidget.ROBOT_SIZE, RobotWidget.ROBOT_SIZE))
        surface.fill(RobotWidget.ROBOT_COLOR)
        return surface

    @override
    def render(self) -> pg.Surface:
        return self._make_robot_surface()

    @override
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        ...

    @override
    def on_robot_crashed(self, robot: Robot) -> None:
        RobotWidget.ROBOT_COLOR = pg.color.THECOLORS['black']

    @override
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        ...
