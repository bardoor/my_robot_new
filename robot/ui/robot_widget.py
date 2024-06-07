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
    ROBOT_ALIVE_COLOR = pg.color.THECOLORS['darkgreen']
    ROBOT_CRASHED_COLOR = pg.color.THECOLORS['red']

    def __init__(self, robot: Robot) -> None:
        self._robot = robot
        self._robot.add_listener(self)
        self._robot_alive = True

    def _make_robot_surface(self) -> pg.Surface:
        surface = pg.Surface((RobotWidget.ROBOT_SIZE, RobotWidget.ROBOT_SIZE))
        surface.fill(RobotWidget.ROBOT_ALIVE_COLOR if self._robot_alive else RobotWidget.ROBOT_CRASHED_COLOR)
        return surface

    @override
    def render(self) -> pg.Surface:
        return self._make_robot_surface()

    @override
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        ...

    @override
    def on_robot_crashed(self, robot: Robot) -> None:
        self._robot_alive = False

    @override
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        ...

    @override
    def handle_event(self, event: pg.event.Event):
        pass

    @override
    def update(self):
        pass
