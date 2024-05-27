from __future__ import annotations
import typing

from robot.model.field.wall import Wall
from robot.model.direction import Direction


# Чтобы избежать циклического импорта...
if typing.TYPE_CHECKING:
    from robot.model.robot import Robot


class Cell:
    _paints_count: int
    _walls: dict[Direction, Wall]
    _robot: Robot
    _neighbors: dict[Direction, Cell]

    def __init__(self):
        self._paints_count = 0
        self._walls = {}
        self._neighbors = {}
        self._robot = None

    def has_wall(self, direction: Direction) -> bool:
        return self.get_wall(direction) is not None

    def set_wall(self, direction: Direction, wall: Wall | None) -> None:
        if self.has_wall(direction) and self.get_wall(direction) != wall:
            raise ValueError("A wall is already set")

        if wall is None:
            self._walls[direction] = None
            self.get_neighbor(direction).set_wall(direction.opposite(), None)
            return

        self._walls[direction] = wall
        if self.has_neighbor(direction) \
                and (n := self.get_neighbor(direction).get_wall(direction.opposite())) != wall:
            self.get_neighbor(direction).set_wall(direction.opposite(), wall)

    def get_wall(self, direction: Direction) -> Wall | None:
        if direction in self._walls:
            return self._walls[direction]
        return None

    def has_neighbor(self, direction: Direction) -> bool:
        return self.get_neighbor(direction) is not None

    def set_neighbor(self, direction: Direction, neighbor: Cell | None) -> None:
        if (self.get_neighbor(direction) not in {None, neighbor}) \
                or (neighbor.get_neighbor(direction.opposite()) not in {None, self}):
            raise ValueError('"neighbor" cannot be set as a neighbor, because it has its own neighbor already')
        
        if neighbor is None:
            t = self._neighbors[direction]
            self._neighbors[direction] = None
            t.set_neighbor(direction.opposite(), None)
            return

        self._neighbors[direction] = neighbor
        if self.has_wall(direction):
            neighbor.set_wall(direction.opposite(), self.get_wall(direction))
        if neighbor.get_neighbor(direction.opposite()) is None:
            neighbor.set_neighbor(direction.opposite(), self)

        # Вот и умерли когда-то,
        # здесь все три богатыря... 
        # На питоне в строках кода
        # разобраться не смогя...
        if (clockwise := self.get_neighbor(direction.clockwise())) is not None:
            if (clockwise := clockwise.get_neighbor(direction)) is not None \
                    and clockwise.get_neighbor(direction.anticlockwise()) != neighbor:
                clockwise.set_neighbor(direction.anticlockwise(), neighbor)
        if (anticlockwise := self.get_neighbor(direction.anticlockwise())) is not None:
            if (anticlockwise := anticlockwise.get_neighbor(direction)) is not None \
                    and anticlockwise.get_neighbor(direction.clockwise()) != neighbor:
                anticlockwise.set_neighbor(direction.clockwise(), neighbor)

    def get_neighbor(self, direction: Direction) -> Cell | None:
        if direction in self._neighbors:
            return self._neighbors[direction]
        return None

    def walls(self):
        return iter(self._walls)

    def neighbors(self):
        return self._neighbors

    def get_robot(self) -> Robot | None:
        return self._robot

    def set_robot(self, new_robot: Robot | None) -> None:
        if new_robot is None and self._robot is not None:
            old_robot = self._robot
            self._robot = None
            old_robot.set_cell(None)
            return

        self._robot = new_robot

        if (self._robot is not None) and (self is not new_robot.cell):
            new_robot.set_cell(self)

    def is_painted(self) -> bool:
        return self._paints_count > 0

    def paints_count(self) -> int:
        return self._paints_count

    def paint(self) -> None:
        self._paints_count += 1