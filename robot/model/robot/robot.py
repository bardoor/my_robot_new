from __future__ import annotations
from enum import Enum

from ..direction import Direction
from ..field.cell import Cell
from robot.model.event import RobotListener


class StepResult(Enum):
    # Получилось передвинуться
    OK = 0
    # Врезался в стену
    HIT_WALL = 1
    # Клетки в заданном направлении не оказалось
    NOT_MOVED = 2


class Robot:
    _cell: Cell
    _listeners: list[RobotListener]

    def __init__(self) -> None:
        self._cell = None
        self._listeners = []

    def get_cell(self) -> Cell:
        return self._cell

    def set_cell(self, new_cell: Cell) -> None:
        if new_cell is None and self._cell is not None:
            old_cell = self._cell
            self._cell = None
            old_cell.set_robot(None)
            return

        self._cell = new_cell

        if (self._cell is not None) and (self is not new_cell.robot()):
            self._cell.set_robot(self)

    def step(self, direction: Direction) -> StepResult:
        if self._cell.has_wall(direction):
            self._fire_on_robot_crashed()
            return StepResult.HIT_WALL

        neighbor = self._cell.get_neighbor(direction)
        if neighbor is None:
            self._fire_on_robot_crashed()
            return StepResult.NOT_MOVED

        old_cell = self._cell
        self._cell.set_robot(None)
        neighbor.set_robot(self)
        self._cell = neighbor
        self._fire_on_robot_moved(old_cell, self._cell)
        return StepResult.OK

    def is_wall(self, direction: Direction) -> bool:
        return self._cell.has_wall(direction)

    def paint(self) -> bool:
        self._cell.paint()
        self._fire_on_robot_painted_cell(self._cell)
        return True

    def add_listener(self, listener: RobotListener) -> None:
        self._listeners.append(listener)

    def remove_listener(self, listener: RobotListener) -> None:
        self._listeners.remove(listener)

    def _fire_on_robot_moved(self, from_cell: Cell, to_cell: Cell) -> None:
        for listener in self._listeners:
            listener.on_robot_moved(self, from_cell, to_cell)

    def _fire_on_robot_crashed(self) -> None:
        for listener in self._listeners:
            listener.on_robot_crashed(self)

    def _fire_on_robot_painted_cell(self, painted_cell: Cell) -> None:
        for listener in self._listeners:
            listener.on_robot_painted_cell(self, painted_cell)


