from typing import Iterable

from .cell import Cell
from ..robot.robot import Robot
from ..direction import Direction
import xml.etree.ElementTree as et
from .exceptions import *


# TODO сделать класс seeder, который будет брать обстановку в файле (или ещё где-то)
# и заполнять поле, а оно автоматически будет ставить ссылки на соседей
# возможно методы типа add_in_row(), add_in_col()
class Field:

    def __init__(self, height: int, width: int) -> None:
        self._validate(height, width)
        self._height = height
        self._width = width

        self._left_top_cell = None
        self._cells_map = {}
        self._generate_field()

    def _validate(self, height: int, width: int) -> None:
        if not isinstance(height, int) or not isinstance(width, int):
            raise TypeError('"height" and "width" both must be int type')
        if height <= 0 or width <= 0:
            raise ValueError('"height" and "width" both must be positive numbers')

    def size(self) -> tuple[int, int]:
        return (self._height, self._width)

    def width(self) -> int:
        return self._width
    
    def height(self) -> int:
        return self._height

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

    def _generate_field(self):
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

    def _generate(self):
        root = et.parse(environment_path).getroot()
        rows = root.findall("row")

        self._height = len(rows)
        self._width = len(rows[0])

        # TODO проверка корректности расстановки стен
        # TODO Вынести это всё в сущность парсер, чтоб поле не знало о файлике с обстановкой

        for row in rows:
            if len(row) != self._width:
                raise RowSizeException(self._width, len(row))

            cells = row.findall("cell")
            for cell in cells:
                cell_walls = []

                if (walls := cell.get("walls", None)) is not None:
                    walls = walls.split(" ")
                    for direction in walls:
                        cell_walls.append(Direction.from_str(direction))

                cell_is_painted = cell.get("painted") == "True"
                robot = Robot() if cell.get("robot") == "True" else None
                self._cells.append(Cell(cell_is_painted, cell_walls, robot))

        self._set_neighbors()

    def _set_neighbors(self):
        cells_matrix = self._as_matrix()
        for row in range(0, self._height):
            for col in range(0, self._width):
                if row > 0:
                    cells_matrix[row][col].set_neighbor(Direction.NORTH, cells_matrix[row - 1][col])
                if row < self._height - 1:
                    cells_matrix[row][col].set_neighbor(Direction.SOUTH, cells_matrix[row + 1][col])
                if col > 0:
                    cells_matrix[row][col].set_neighbor(Direction.WEST, cells_matrix[row][col - 1])
                if col < self._width - 1:
                    cells_matrix[row][col].set_neighbor(Direction.EAST, cells_matrix[row][col + 1])

    def _as_matrix(self):
        matrix = []

        for i in range(0, len(self._cells), self._width):
            row = self._cells[i: i + self._width]
            matrix.append(row)

        return matrix

    def robot(self):
        for cell in self._cells:
            if cell.robot is not None:
                return cell.robot
