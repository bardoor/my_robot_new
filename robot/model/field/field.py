from typing import Iterable
import json

from .cell import Cell
from ..robot.robot import Robot
from ..direction import Direction
import xml.etree.ElementTree as et
from .exceptions import *


# TODO сделать класс seeder, который будет брать обстановку в файле (или ещё где-то)
# и заполнять поле, а оно автоматически будет ставить ссылки на соседей
# возможно методы типа add_in_row(), add_in_col()
class Field:

    def __init__(self, width: int, height: int) -> None:
        self._validate(width, height)
        self._width = width
        self._height = height

        self._left_top_cell = None
        self._cells_map = {}
        self._generate_field()

    def _validate(self, width: int, height: int) -> None:
        if height <= 0 or width <= 0:
            raise ValueError('"height" and "width" both must be positive numbers')
        if not isinstance(height, int) or not isinstance(width, int):
            raise TypeError('"height" and "width" both must be int type')

    def dump(self, env_file_name: str) -> None:
        env_config = {'height': self.height(), 'width': self.width()}

        walls = self._get_walls()
        env_config['walls'] = walls

        painted = self._get_painted_pos()
        env_config['painted'] = painted

        robot = self._get_robot_pos()
        env_config['robot'] = robot

        with open(env_file_name, 'w') as output:
            json.dump(env_config, output)

    def size(self) -> tuple[int, int]:
        return (self._width, self._height)

    def width(self) -> int:
        return self._width
    
    def height(self) -> int:
        return self._height

    def _get_walls(self) -> list[tuple[int, int]]:
        seen_walls = []
        walls_info = []
        
        for x in range(self._width):
            for y in range(self._height):
                cell = self.get_cell(x, y)

                for direction, wall in cell.walls().items():
                    if wall not in seen_walls:
                        seen_walls.append(wall)
                        walls_info.append({"x": x, "y": y, "direction": str(direction)})

        return walls_info

    def _get_painted_pos(self) -> list[tuple[int, int]]:
        painted = []
        for x in range(self._width):
            for y in range(self._height):
                if self.get_cell(x, y).is_painted():
                    painted.append({'x': x, 'y': y})
        return painted

    def _get_robot_pos(self) -> tuple[int, int] | None:
        for x in range(self._width):
            for y in range(self._height):
                if self.get_cell(x, y).get_robot() is not None:
                    return {'x': x, 'y': y}
        return None

    def _get_pos(self, cell: Cell) -> tuple[int, int] | None:
        # Зачем нужен метод, который по переданной клетке, возвращает её позицию на поле?
        # Только для сериализации обстановки: чтобы, например, пройтись по всем клеткам,
        # найти только закрашенные и сереализовать их коориданаты в файле.
        # Все что здесь происходит жутко алгоритмически неэффективно...
        for x in range(self._width):
            for y in range(self._height):
                if self.get_cell(x, y) == cell:
                    return (x, y)
        return None

    def get_cell(self, x: int, y: int) -> Cell:
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('"x" and "y" both must be int type')
        if x < 0 or x >= self._width:
            raise ValueError(f'"x" must be in range 0..{self._width - 1}')
        if y < 0 or y >= self._height:
            raise ValueError(f'"y" must be in range 0..{self._height - 1}')
        
        current_x, current_y = x, y

        current_cell = self._left_top_cell
        while current_x > 0:
            current_cell = current_cell.get_neighbor(Direction.EAST)
            current_x -= 1
        while current_y > 0:
            current_cell = current_cell.get_neighbor(Direction.SOUTH)
            current_y -= 1

        return current_cell

    def cells(self) -> Iterable[Cell]:
        visited = set()

        need_to_visit = [self._left_top_cell]
        while need_to_visit:
            cell = need_to_visit.pop()

            for neighbor in cell.neighbors().values():
                if (neighbor not in need_to_visit) and (neighbor not in visited):
                    need_to_visit.append(neighbor)

            visited.add(cell)

        return visited

    def add_row(self) -> None:
        new_row = Cell()
        self._cells_map['left_bottom'].set_neighbor(Direction.SOUTH, new_row)
        self._cells_map['left_bottom'] = new_row

        for _ in range(1, self._width):
            next_cell = Cell()
            new_row.set_neighbor(Direction.EAST, next_cell)
            new_row = next_cell

        self._height += 1

    def add_col(self) -> None:
        new_col = Cell()
        self._cells_map['right_top'].set_neighbor(Direction.EAST, new_col)
        self._cells_map['right_top'] = new_col

        for _ in range(1, self._height):
            next_cell = Cell()
            new_col.set_neighbor(Direction.SOUTH, next_cell)
            new_col = next_cell
        
        self._width += 1

    def remove_row(self) -> None:
        if self._height == 1:
            raise RuntimeError("Cannot remove the last row")
        
        need_to_remove = []
        for i in range(self._width):
            need_to_remove.append(self.get_cell(i, self._height - 1))
        
        # Возможно тут надо как-то более хитро удалять, чтобы не было
        # висячих ссылок или типа того, но как же мне лень в этом разбираться...
        for cell in need_to_remove:
            cell.set_neighbor(Direction.NORTH, None)

        self._cells_map['left_bottom'] = self.get_cell(0, self._height - 2)

        self._height -= 1

    def remove_col(self) -> None:
        if self._width == 1:
            raise RuntimeError("Cannot remove the last column")
        
        need_to_remove = []
        for i in range(self._height):
            need_to_remove.append(self.get_cell(self._width - 1, i))
        
        # Возможно тут надо как-то более хитро удалять, чтобы не было
        # висячих ссылок или типа того, но как же мне лень в этом разбираться...
        for cell in need_to_remove:
            cell.set_neighbor(Direction.WEST, None)
        
        self._cells_map['right_top'] = self.get_cell(self._width - 2, 0)

        self._width -= 1

    def _generate_field(self) -> None:
        self._left_top_cell = Cell()

        self._cells_map['right_top'] = self._left_top_cell
        self._cells_map['left_bottom'] = self._left_top_cell

        current_row = self._left_top_cell
        for i in range(self._height):
            current_col = current_row

            for j in range(1, self._width):
                next_cell = Cell()
                current_col.set_neighbor(Direction.EAST, next_cell)
                current_col = next_cell

                if i == 0 and j == self._width-1:
                    self._cells_map['right_top'] = current_col

            if i + 1 < self._height:
                next_row = Cell()
                current_row.set_neighbor(Direction.SOUTH, next_row)
                current_row = next_row

                self._cells_map['left_bottom'] = current_row

    def robot(self):
        for cell in self._cells:
            if cell.robot is not None:
                return cell.robot
