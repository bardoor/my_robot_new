from __future__ import annotations
from typing import override, TYPE_CHECKING

import pygame as pg

from robot.ui.core.widget import Widget
from robot.ui.cell_widget import CellWidget
from robot.model.direction import Direction

from robot.model.field import Wall

if TYPE_CHECKING:
    from robot.model.field import Cell


class WallWidget(Widget):
    WIDTH = 10
    LENGTH = CellWidget.CELL_SIZE + WIDTH
    COLOR = pg.color.THECOLORS['purple']

    def __init__(self, cell: Cell, direction: Direction, wall: Wall = None) -> None:
        self._wall = wall
        self._cell = cell
        self._direction = direction

    @override
    def size(self) -> tuple[int, int]:
        return (WallWidget.WIDTH, WallWidget.LENGTH)

    @override
    def render(self) -> pg.Surface:
        if self._wall is not None:
            WallWidget.COLOR = pg.color.THECOLORS['purple']
        else:
            WallWidget.COLOR = pg.color.THECOLORS['black']

        if self._direction in {Direction.NORTH, Direction.SOUTH}:
            wall_surface = pg.Surface((WallWidget.LENGTH, WallWidget.WIDTH))
        elif self._direction in {Direction.EAST, Direction.WEST}:
            wall_surface = pg.Surface((WallWidget.WIDTH, WallWidget.LENGTH))
        else:
            raise ValueError(f"Unsupported direction: {self._direction}")
        
        wall_surface.fill(WallWidget.COLOR)
        return wall_surface

    def remove_wall(self):
        self._cell.set_wall(self._direction, None)
        self._wall = None

    def set_wall(self, wall: Wall):
        self._cell.set_wall(self._direction, wall)
        self._wall = wall

    @override
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self._wall is not None:
                self.remove_wall()
            else:
                self.set_wall(Wall(self._direction, self._cell))

    @override
    def update(self):
        pass
