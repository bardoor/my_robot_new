from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.ui.core.widget import Widget
from robot.ui.cell_widget import CellWidget
from robot.model.direction import Direction


if TYPE_CHECKING:
    from robot.model.field import Wall


class WallWidget(Widget):
    WIDTH = 10
    LENGTH = CellWidget.CELL_SIZE + WIDTH
    COLOR = pg.color.THECOLORS['purple']

    def __init__(self, wall: Wall) -> None:
        self._wall = wall
        self._direction = self._wall.direction()

    @override
    def size(self) -> tuple[int, int]:
        return (WallWidget.WIDTH, WallWidget.LENGTH)

    @override
    def render(self) -> pg.Surface:
        if self._direction in {Direction.NORTH, Direction.SOUTH}:
            wall_surface = pg.Surface((WallWidget.LENGTH, WallWidget.WIDTH))
        elif self._direction in {Direction.EAST, Direction.WEST}:
            wall_surface = pg.Surface((WallWidget.WIDTH, WallWidget.LENGTH))
        else:
            raise ValueError(f"Unsupported direction: {self._direction}")
        
        wall_surface.fill(WallWidget.COLOR)
        return wall_surface

    @override
    def handle_event(self, event: pg.event.Event):
        pass

    @override
    def update(self):
        pass
