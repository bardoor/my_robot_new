from __future__ import annotations
from typing import TYPE_CHECKING
from robot.model.direction import Direction

if TYPE_CHECKING:
    from robot.model.field.cell import Cell


class Wall:

    def __init__(self, direction: Direction, cell: Cell) -> None:
        self._direction = direction  # Направление стены относительно клетки
        self._cell = cell

    def direction(self) -> Direction:
        return self._direction

    def cell(self) -> Cell:
        return self._cell

    def destroy(self):
        self._cell.remove_wall(self._direction)
