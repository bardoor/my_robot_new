from __future__ import annotations
import typing

from robot.model.field.wall import Wall
from robot.model.direction import Direction
from robot.model.event.listeners import CellListener


# Чтобы избежать циклического импорта...
if typing.TYPE_CHECKING:
    from robot.model.robot import Robot


class Cell:
    _paints_count: int
    _walls: dict[Direction, Wall]
    _robot: Robot
    _neighbors: dict[Direction, Cell]
    _listeners: list[CellListener]

    def __init__(self):
        self._paints_count = 0
        self._walls = {}
        self._neighbors = {}
        self._robot = None
        self._listeners = []

    def has_wall(self, direction: Direction) -> bool:
        return self.get_wall(direction) is not None

    def remove_wall(self, direction:Direction) -> None:
        if not self.has_wall(direction):
            raise ValueError(f"There is no wall at {direction}")
        del self._walls[direction]

    def set_wall(self, direction: Direction, wall: Wall | None) -> None:
        # Удаляем стену, если в указанном направлении она есть, а переданная стена - None
        if wall is None and self._walls[direction] is not None:
            self._walls[direction] = None
            self.get_neighbor(direction).set_wall(direction.opposite(), None)
            return

        # Ругаемся если стена в указанном направлении уже установлена
        if self.has_wall(direction) and self.get_wall(direction) != wall:
            raise ValueError("A wall is already set")

        # Ставим стену в указанном направлении себе и своему соседу (если он есть)
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
        # Удаляем соседа в направлении, если он уже есть, а переданный сосед - None
        if neighbor is None:
            prev_neighbor = self._neighbors.get(direction, None)
            if prev_neighbor is not None:
                # Удаляем информацию о соседе у себя
                del self._neighbors[direction]

                # Просим соседа забыть нас
                if prev_neighbor.get_neighbor(direction.opposite()) == self:
                    prev_neighbor.set_neighbor(direction.opposite(), None)
            return

        # Ругаемся если у нас или у переданного соседа есть соседи в желаемых направлениях
        if (self.get_neighbor(direction) not in {None, neighbor}) \
                or (neighbor.get_neighbor(direction.opposite()) not in {None, self}):
            raise ValueError('"neighbor" cannot be set as a neighbor, because it has its own neighbor already')

        self._neighbors[direction] = neighbor
        if self.has_wall(direction):
            neighbor.set_wall(direction.opposite(), self.get_wall(direction))
        if neighbor.get_neighbor(direction.opposite()) is None:
            neighbor.set_neighbor(direction.opposite(), self)

        # Вот и умерли когда-то,
        # здесь все три богатыря... 
        # На питоне в строках кода
        # разобраться не смогя...
        # Если у нас есть сосед по часовой стрелке от переданного направления
        if (clockwise := self.get_neighbor(direction.clockwise())) is not None:
            # ... Берём этого соседа и если у него есть сосед в оригинальном направлении
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

    def walls(self) -> dict[Direction, Wall]:
        return self._walls

    def neighbors(self) -> dict[Direction, Cell]:
        return self._neighbors

    def robot(self) -> Robot | None:
        return self._robot

    def has_robot(self) -> bool:
        return self.robot() is not None

    def set_robot(self, new_robot: Robot | None) -> None:
        if new_robot is None and self._robot is not None:
            old_robot = self._robot
            self._robot = None
            old_robot.set_cell(None)
            self._fire_robot_left_cell()
            return

        self._robot = new_robot

        if (self._robot is not None) and (self is not new_robot.get_cell()):
            new_robot.set_cell(self)
            self._fire_robot_arrived_in_cell()

    def is_painted(self) -> bool:
        return self._paints_count > 0

    def paints_count(self) -> int:
        return self._paints_count

    def paint(self) -> None:
        self._paints_count += 1
        self._fire_cell_got_painted()

    def unpaint(self) -> None:
        self._paints_count = 0

    def add_listener(self, listener: CellListener) -> None:
        self._listeners.append(listener)

    def remove_listener(self, listener: CellListener) -> None:
        self._listeners.remove(listener)

    def _fire_robot_left_cell(self) -> None:
        for listener in self._listeners:
            listener.on_robot_left_cell(self.robot(), self)

    def _fire_robot_arrived_in_cell(self) -> None:
        for listener in self._listeners:
            listener.on_robot_arrived_in_cell(self.robot(), self)

    def _fire_cell_got_painted(self) -> None:
        for listener in self._listeners:
            listener.on_cell_got_painted(self)