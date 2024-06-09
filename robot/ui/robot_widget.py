from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg
import pygame.draw

from robot.model.event import RobotListener
from robot.ui.core import Widget
from robot.model.direction import Direction


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
        self._robot_crashed_side = None

    def _make_crashed_rect(self, direction: Direction, surface: pg.Surface) -> None:
        topleft = surface.get_rect().topleft
        w, h = surface.get_size()

        # Определяем координаты прямоугольника в зависимости от направления
        match direction:
            case Direction.EAST:
                topleft = (topleft[0] + w // 2, topleft[1])
                w = w // 2
            case Direction.SOUTH:
                topleft = (topleft[0], topleft[1] + h // 2)
                h = h // 2
            case Direction.NORTH:
                h = h // 2
            case Direction.WEST:
                w = w // 2

        pygame.draw.rect(surface, RobotWidget.ROBOT_CRASHED_COLOR, pg.Rect(topleft, (w, h)))

    def _make_robot_surface(self) -> pg.Surface:
        surface = pg.Surface((RobotWidget.ROBOT_SIZE, RobotWidget.ROBOT_SIZE))
        surface.fill(RobotWidget.ROBOT_ALIVE_COLOR)
        if not self._robot_alive:
            self._make_crashed_rect(self._robot_crashed_side, surface)
        return surface

    @override
    def render(self) -> pg.Surface:
        return self._make_robot_surface()

    @override
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        ...

    @override
    def on_robot_crashed(self, robot: Robot, direction: Direction) -> None:
        self._robot_alive = False
        self._robot_crashed_side = direction

    @override
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        ...

    @override
    def handle_event(self, event: pg.event.Event):
        pass

    @override
    def update(self):
        pass
