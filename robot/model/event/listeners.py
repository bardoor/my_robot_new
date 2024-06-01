from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from robot.model.field import Cell


class RobotListener(ABC):

    @abstractmethod
    def on_robot_moved(self, from_cell: Cell, to_cell: Cell) -> None:
        ...

    @abstractmethod
    def on_robot_not_moved(self) -> None:
        ...

    @abstractmethod
    def on_robot_painted_cell(self) -> None:
        ...


class CellListener(ABC):

    @abstractmethod
    def on_cell_got_painted(self) -> None:
        ...

    @abstractmethod
    def on_robot_left_cell(self) -> None:
        ...

    @abstractmethod
    def on_robot_arrived_in_cell(self) -> None:
        ...