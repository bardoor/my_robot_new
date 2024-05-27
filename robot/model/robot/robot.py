from enum import Enum

from ..direction import Direction
from ..field.cell import Cell


class StepResult(Enum):
    # Получилось передвинуться
    OK = 0
    # Врезался в стену
    HIT_WALL = 1
    # Клетки в заданном направлении не оказалось
    NOT_MOVED = 2


class Robot:
    _cell: Cell

    def __init__(self) -> None:
        self._cell = None

    def get_cell(self) -> Cell:
        return self._cell

    def set_cell(self, new_cell: Cell) -> None:
        if new_cell is None and self._cell is not None:
            old_cell = self._cell
            self._cell = None
            old_cell.set_robot(None)
            return

        self._cell = new_cell

        if (self._cell is not None) and (self is not new_cell.robot):
            old_cell.set_robot(self)

    def step(self, direction: Direction) -> StepResult:
        if self._cell.has_wall(direction):
            return StepResult.HIT_WALL

        neighbor = self._cell.get_neighbor(direction)
        if neighbor is None:
            return StepResult.NOT_MOVED

        self._cell.set_robot(None)
        neighbor.set_robot(self)
        self._cell = neighbor
        return StepResult.OK

    def is_wall(self, direction: Direction) -> bool:
        return self._cell.has_wall(direction)

    def paint(self) -> bool:
        self._cell.paint()
        return True

