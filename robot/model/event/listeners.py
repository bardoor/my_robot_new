from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from robot.model.direction import Direction

if TYPE_CHECKING:
    from robot.model.field import Cell
    from robot.model.robot import Robot


class RobotListener(ABC):

    @abstractmethod
    def on_robot_moved(self, robot: Robot, from_cell: Cell, to_cell: Cell) -> None:
        ...

    @abstractmethod
    def on_robot_painted_cell(self, robot: Robot, painted_cell: Cell) -> None:
        ...

    @abstractmethod
    def on_robot_crashed(self, robot: Robot, direction: Direction) -> None:
        ...


class CellListener(ABC):

    @abstractmethod
    def on_cell_got_painted(self, cell: Cell) -> None:
        ...

    @abstractmethod
    def on_robot_left_cell(self, robot: Robot, left_cell: Cell) -> None:
        ...

    @abstractmethod
    def on_robot_arrived_in_cell(self, robot: Robot, arrived_cell: Cell) -> None:
        ...